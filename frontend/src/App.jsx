import { useState } from 'react';
import { debateApi } from './api/debate';
function App() {
  const [topic, setTopic] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [currentRound, setCurrentRound] = useState(0);
  const [rounds, setRounds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('idle');
  const [judgment, setJudgment] = useState(null);
  const [error, setError] = useState('');
  const handleStart = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    setLoading(true);
    setError('');
    try {
      const result = await debateApi.startDebate(topic);
      setSessionId(result.session_id);
      setStatus('started');
      setCurrentRound(0);
      setRounds([]);
    } catch (err) {
      setError('Failed to start debate. Please check your API keys.');
    } finally {
      setLoading(false);
    }
  };
  const handleNextRound = async () => {
    if (!sessionId) return;
    setLoading(true);
    setError('');
    try {
      const result = await debateApi.executeRound(sessionId);
      if (result.current_round) {
        setRounds([...rounds, result.current_round]);
        setCurrentRound(currentRound + 1);
      }
      if (result.is_complete) {
        setStatus('rounds_complete');
      }
    } catch (err) {
      setError('Failed to execute round.');
    } finally {
      setLoading(false);
    }
  };
  const handleGetJudgment = async () => {
    if (!sessionId) return;
    setLoading(true);
    setError('');
    try {
      const result = await debateApi.getJudgment(sessionId);
      setJudgment(result.judge_evaluation);
      setStatus('complete');
    } catch (err) {
      setError('Failed to get judgment.');
    } finally {
      setLoading(false);
    }
  };
  const handleReset = () => {
    setTopic('');
    setSessionId(null);
    setCurrentRound(0);
    setRounds([]);
    setJudgment(null);
    setStatus('idle');
    setError('');
  };
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">
          AI Debate Engine
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Two AI agents debate your topic with real-time fact-checking
        </p>
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        {status === 'idle' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={handleStart}>
              <label className="block text-gray-700 font-semibold mb-2">
                Debate Topic
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Should AI be regulated?"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="submit"
                disabled={loading || !topic.trim()}
                className="mt-4 w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Starting...' : 'Start Debate'}
              </button>
            </form>
          </div>
        )}
        {status === 'started' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">
                Topic: {topic}
              </h2>
              <p className="text-gray-600">
                Round {currentRound} of 3
              </p>
            </div>
            {rounds.map((round, idx) => (
              <RoundCard key={idx} round={round} />
            ))}
            <div className="flex gap-4">
              {currentRound < 3 ? (
                <button
                  onClick={handleNextRound}
                  disabled={loading}
                  className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition"
                >
                  {loading ? 'Processing...' : `Start Round ${currentRound + 1}`}
                </button>
              ) : (
                <button
                  onClick={handleGetJudgment}
                  disabled={loading}
                  className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 transition"
                >
                  {loading ? 'Evaluating...' : 'Get Judge Evaluation'}
                </button>
              )}
            </div>
          </div>
        )}
        {status === 'complete' && judgment && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-center mb-6">Debate Results</h2>
              <div className="text-center mb-6">
                <span className="text-lg text-gray-600">Winner: </span>
                <span className={`text-3xl font-bold ${
                  judgment.winner === 'Pro' ? 'text-green-600' : 
                  judgment.winner === 'Con' ? 'text-red-600' : 'text-gray-600'
                }`}>
                  {judgment.winner}
                </span>
              </div>
              <div className="flex justify-center gap-12 mb-6">
                <div className="text-center">
                  <p className="text-gray-600">Pro Score</p>
                  <p className="text-4xl font-bold text-green-600">{judgment.pro_score}/10</p>
                </div>
                <div className="text-center">
                  <p className="text-gray-600">Con Score</p>
                  <p className="text-4xl font-bold text-red-600">{judgment.con_score}/10</p>
                </div>
              </div>
              {judgment.feedback && judgment.feedback.length > 0 && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2">Judge Feedback:</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-700">
                    {judgment.feedback.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <button
              onClick={handleReset}
              className="w-full bg-gray-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-700 transition"
            >
              Start New Debate
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
function RoundCard({ round }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="bg-gray-800 text-white px-6 py-3">
        <h3 className="font-semibold">Round {round.round_number}</h3>
      </div>
      <div className="p-6 space-y-4">
        <div className="border-l-4 border-green-500 pl-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm font-semibold">
              PRO
            </span>
          </div>
          <p className="text-gray-700 whitespace-pre-wrap">{round.pro_argument.content}</p>
          {round.pro_argument.fact_checks && round.pro_argument.fact_checks.length > 0 && (
            <FactChecks checks={round.pro_argument.fact_checks} />
          )}
        </div>
        <div className="border-l-4 border-red-500 pl-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-semibold">
              CON
            </span>
          </div>
          <p className="text-gray-700 whitespace-pre-wrap">{round.con_argument.content}</p>
          {round.con_argument.fact_checks && round.con_argument.fact_checks.length > 0 && (
            <FactChecks checks={round.con_argument.fact_checks} />
          )}
        </div>
      </div>
    </div>
  );
}
function FactChecks({ checks }) {
  return (
    <div className="mt-3 pt-3 border-t border-gray-200">
      <p className="text-sm font-semibold text-gray-600 mb-2">Fact Check:</p>
      {checks.map((check, idx) => (
        <div key={idx} className={`text-sm p-2 rounded mb-1 ${check.is_verified ? 'bg-green-50' : 'bg-yellow-50'}`}>
          <span className={`font-medium ${check.is_verified ? 'text-green-700' : 'text-yellow-700'}`}>
            {check.is_verified ? '✓ Verified' : '⚠ Unverified'}:
          </span>
          <span className="text-gray-600 ml-1">{check.claim}</span>
        </div>
      ))}
    </div>
  );
}
export default App;