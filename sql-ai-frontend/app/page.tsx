"use client";
import React, { useState } from 'react';
import { Database, Send, Terminal, Table as TableIcon, Zap, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SQLDashboard() {
  const [dbUrl, setDbUrl] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleConnect = async () => {
    const res = await fetch('http://127.0.0.1:8000/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ db_url: dbUrl })
    });
    if (res.ok) setIsConnected(true);
  };

    const handleAsk = async () => {
      if (!question) return;
      setLoading(true);
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      setChatHistory([...chatHistory, { question, ...data }]);
      setQuestion("");
      setLoading(false);
    };

    return (
      <div className="min-h-screen bg-[#0B0E14] text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Sidebar / Connection Bar */}
      <nav className="border-b border-slate-800 bg-[#0B0E14]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <div className="flex items-center gap-2">
      <div className="bg-indigo-600 p-1.5 rounded-lg">
      <Zap size={20} className="text-white fill-current" />
      </div>
      <span className="font-bold text-xl tracking-tight text-white">Insight<span className="text-indigo-500">SQL</span></span>
      </div>

      <div className="flex items-center gap-4">
      <input
      type="text"
      placeholder="postgresql://user:pass@localhost:5432/db"
      className="bg-slate-900/50 border border-slate-700 rounded-full px-4 py-1.5 text-sm w-80 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
      value={dbUrl}
      onChange={(e) => setDbUrl(e.target.value)}
      />
      <button
      onClick={handleConnect}
      className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium transition-all ${isConnected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}`}
      >
      {isConnected ? <><CheckCircle2 size={16}/> Connected</> : <><Database size={16}/> Connect DB</>}
      </button>
      </div>
      </div>
      </nav>

      <main className="max-w-5xl mx-auto py-10 px-6">
      {/* Chat History */}
      <div className="space-y-8 mb-32">
      {chatHistory.map((item, idx) => (
        <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        key={idx}
        className="space-y-4"
        >
        {/* User Question */}
        <div className="flex justify-end">
        <div className="bg-indigo-600 text-white px-5 py-3 rounded-2xl rounded-tr-none max-w-[80%] shadow-lg shadow-indigo-500/10">
        {item.question}
        </div>
        </div>

        {/* AI Response */}
        <div className="flex justify-start">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-6 w-full shadow-xl">
        <p className="text-slate-400 mb-6 leading-relaxed">{item.explanation}</p>

        {/* SQL Block */}
        <div className="bg-[#05070a] rounded-xl p-4 border border-slate-800 mb-6 group relative">
        <div className="flex items-center gap-2 mb-2 text-xs font-mono text-slate-500 uppercase tracking-widest">
        <Terminal size={14} /> Generated SQL
        </div>
        <pre className="text-indigo-300 font-mono text-sm overflow-x-auto">
        {item.sql}
        </pre>
        </div>

        {/* Results Table */}
        <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
        <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-800 bg-slate-800/30 text-xs font-semibold text-slate-400 uppercase">
        <TableIcon size={14} /> Result Set
        </div>
        <div className="overflow-x-auto">
        <table className="w-full text-left text-sm border-collapse">
        <thead>
        <tr className="bg-slate-800/50">
        {Object.keys(item.result[0] || {}).map(key => (
          <th key={key} className="px-4 py-3 font-medium text-slate-300 capitalize">{key.replace('_', ' ')}</th>
        ))}
        </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
        {item.result.map((row: any, i: number) => (
          <tr key={i} className="hover:bg-slate-800/30 transition-colors">
          {Object.values(row).map((val: any, j: number) => (
            <td key={j} className="px-4 py-3 text-slate-400">{val}</td>
          ))}
          </tr>
        ))}
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </motion.div>
      ))}
      {loading && (
        <div className="flex justify-start animate-pulse">
        <div className="bg-slate-900 h-32 w-full rounded-2xl border border-slate-800"></div>
        </div>
      )}
      </div>

      {/* Floating Input Area */}
      <div className="fixed bottom-8 left-0 right-0 max-w-3xl mx-auto px-6">
      <div className="relative group">
      <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-25 group-focus-within:opacity-50 transition duration-1000"></div>
      <div className="relative bg-[#161B22] border border-slate-700 rounded-2xl flex items-center p-2 shadow-2xl">
      <input
      type="text"
      placeholder="Ask your database anything..."
      className="flex-1 bg-transparent px-4 py-3 text-white focus:outline-none"
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
      />
      <button
      onClick={handleAsk}
      disabled={loading || !isConnected}
      className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 text-white p-3 rounded-xl transition-all"
      >
      <Send size={20} />
      </button>
      </div>
      </div>
      <p className="text-center text-slate-500 text-xs mt-4">
      Connected to: <span className="text-indigo-400 font-mono">{dbUrl || 'No Database'}</span>
      </p>
      </div>
      </main>
      </div>
    );
}
