import React, { useState, useRef, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const KnowledgeCurator = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'agent',
      content: '您好，我是知识馆长。我连接着浩瀚的非遗知识图谱，知晓苏绣的针法演变，也懂得紫砂的泥料乾坤，更了解皮影戏的光影艺术。您可以问我："苏绣乱针绣是谁发明的？"、"皮影戏有哪些主要流派？"、"紫砂壶制作需要什么材料？"'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [followUpQuestions, setFollowUpQuestions] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const messagesContainerRef = useRef(null);

  // 滚动到底部
  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      requestAnimationFrame(() => {
        messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
      });
    }
  };

  // 当消息更新时，自动滚动到底部
  useEffect(() => {
    setTimeout(() => scrollToBottom(), 0);
  }, [messages, followUpQuestions, loading]);

  // 从 localStorage 获取或创建 session ID，并加载历史对话
  useEffect(() => {
    let storedSessionId = localStorage.getItem('knowledge_session_id');
    if (!storedSessionId) {
      storedSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('knowledge_session_id', storedSessionId);
    }
    setSessionId(storedSessionId);
    loadHistory(storedSessionId);
  }, []);

  // 加载历史对话
  const loadHistory = async (sessionId) => {
    try {
      const response = await fetch(`http://localhost:8002/api/v1/knowledge/session/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        if (data.history && data.history.length > 0) {
          const historyMessages = [];
          data.history.forEach((item, index) => {
            historyMessages.push({
              id: index * 2,
              sender: 'user',
              content: item.query
            });
            historyMessages.push({
              id: index * 2 + 1,
              sender: 'agent',
              content: item.answer,
              relatedEntities: []
            });
          });
          setMessages(historyMessages);
        }
      }
    } catch (error) {
      console.error('加载历史对话失败:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const handleSend = async (customQuery = null) => {
    const queryToSend = customQuery || input;
    if (!queryToSend.trim()) return;

    const userMsg = { id: Date.now(), sender: 'user', content: queryToSend };
    setMessages(prev => [...prev, userMsg]);

    if (!customQuery) {
      setInput('');
    }
    setFollowUpQuestions([]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8002/api/v1/knowledge/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryToSend,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'agent',
        content: data.answer,
        relatedEntities: data.related_entities
      }]);

      if (data.follow_up_questions && data.follow_up_questions.length > 0) {
        setFollowUpQuestions(data.follow_up_questions);
      }

      if (data.session_id) {
        localStorage.setItem('knowledge_session_id', data.session_id);
        setSessionId(data.session_id);
      }
    } catch (error) {
      console.error('Error fetching knowledge:', error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'agent',
        content: "抱歉，我现在无法连接到知识库，请稍后再试。"
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFollowUpClick = (question) => {
    handleSend(question);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearHistory = () => {
    localStorage.removeItem('knowledge_session_id');
    setMessages([{
      id: 1,
      sender: 'agent',
      content: '您好，我是知识馆长。我连接着浩瀚的非遗知识图谱，知晓苏绣的针法演变，也懂得紫砂的泥料乾坤，更了解皮影戏的光影艺术。您可以问我："苏绣乱针绣是谁发明的？"、"皮影戏有哪些主要流派？"、"紫砂壶制作需要什么材料？"'
    }]);
    setFollowUpQuestions([]);
    const newSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('knowledge_session_id', newSessionId);
    setSessionId(newSessionId);
  };

  // 快捷提问列表
  const quickQuestions = [
    { icon: '🎭', text: '皮影戏的起源和历史', category: '历史' },
    { icon: '🪡', text: '苏绣有哪些针法', category: '工艺' },
    { icon: '🏺', text: '紫砂壶的制作工艺', category: '工艺' },
    { icon: '👤', text: '非遗传承人有哪些', category: '人物' }
  ];

  // Markdown 渲染组件
  const MarkdownContent = ({ content }) => (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
        h1: ({node, ...props}) => <h1 className="font-calligraphy text-lg font-bold mb-2 mt-3" {...props} />,
        h2: ({node, ...props}) => <h2 className="font-calligraphy text-base font-bold mb-2 mt-3" {...props} />,
        h3: ({node, ...props}) => <h3 className="font-xiaowei text-sm font-bold mb-1 mt-2" {...props} />,
        ul: ({node, ...props}) => <ul className="list-disc list-inside mb-2 space-y-1 ml-2" {...props} />,
        ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-2 space-y-1 ml-2" {...props} />,
        li: ({node, ...props}) => <li className="text-xs" {...props} />,
        strong: ({node, ...props}) => <strong className="font-bold text-ink-black" {...props} />,
        em: ({node, ...props}) => <em className="italic" {...props} />,
        code: ({node, inline, ...props}) => (
          inline
            ? <code className="bg-ink-black/5 px-1.5 py-0.5 rounded text-xs font-mono" {...props} />
            : <code className="block bg-ink-black/5 p-2 rounded-sm text-xs font-mono my-2 overflow-x-auto" {...props} />
        ),
        blockquote: ({node, ...props}) => (
          <blockquote className="border-l-2 border-tea-green pl-3 italic text-xs my-2" {...props} />
        ),
        table: ({node, ...props}) => (
          <div className="overflow-x-auto my-2">
            <table className="min-w-full border border-ink-black/10 text-xs" {...props} />
          </div>
        ),
        th: ({node, ...props}) => <th className="border border-ink-black/10 bg-ink-black/5 px-2 py-1.5 font-bold" {...props} />,
        td: ({node, ...props}) => <td className="border border-ink-black/10 px-2 py-1.5" {...props} />,
      }}
    >
      {content}
    </ReactMarkdown>
  );

  return (
    <div className="h-screen bg-rice-paper flex flex-col overflow-hidden">
      <Navbar />

      <main className="flex-grow flex max-w-7xl mx-auto w-full gap-8 p-6 pt-24 overflow-hidden">
        {/* Left Sidebar - 装饰性边栏 */}
        <div className="hidden lg:flex w-64 flex-shrink-0 flex-col gap-4">
          {/* 知识图谱卡片 */}
          <div className="bg-white p-5 card-shadow rounded-sm relative overflow-hidden border-t-4 border-tea-green group hover:shadow-xl transition-all duration-300">
            <div className="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
              <span className="font-calligraphy text-6xl text-tea-green">知</span>
            </div>

            <div className="relative z-10">
              <div className="inline-block mb-3">
                <span className="seal-border text-vermilion text-xs">在线</span>
              </div>

              <h3 className="font-xiaowei text-lg mb-2 text-ink-black">非遗知识图谱</h3>
              <p className="font-serif text-xs text-charcoal/70 mb-3 leading-relaxed">
                连接 Neo4j 图谱，讲述技艺背后的历史与美学
              </p>
            </div>
          </div>

          {/* 快捷提问 */}
          <div className="bg-white p-5 card-shadow rounded-sm relative overflow-hidden border-t-4 border-cyan-glaze group hover:shadow-xl transition-all duration-300 flex-1 overflow-hidden flex flex-col">
            <div className="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
              <span className="font-calligraphy text-6xl text-cyan-glaze">问</span>
            </div>

            <h4 className="font-xiaowei text-base mb-3 relative z-10 text-ink-black">快捷提问</h4>

            <div className="space-y-2 relative z-10 overflow-y-auto">
              {quickQuestions.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(q.text)}
                  disabled={loading}
                  className="w-full text-left p-2.5 rounded-sm bg-rice-paper/80 hover:bg-tea-green/30 border border-ink-black/5 transition-all duration-200 group"
                >
                  <div className="flex items-start gap-2">
                    <span className="text-base">{q.icon}</span>
                    <div className="min-w-0">
                      <p className="text-xs text-charcoal font-serif truncate">{q.text}</p>
                      <span className="text-xs text-charcoal/40">{q.category}</span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 清空历史 */}
          <button
            onClick={handleClearHistory}
            className="w-full p-2.5 text-xs text-charcoal/60 hover:text-vermilion transition-colors font-serif flex items-center justify-center gap-1.5 border border-ink-black/10 rounded-sm hover:bg-vermilion/5"
          >
            <span>🗑️</span>
            清空对话历史
          </button>
        </div>

        {/* Right - Chat Interface */}
        <div className="flex-1 flex flex-col min-h-0">
          <div className="bg-white card-shadow rounded-sm relative overflow-hidden flex flex-col h-full">
            {/* 装饰性背景 */}
            <div className="absolute top-0 right-0 w-32 h-32 border border-ink-black/3 rounded-full"></div>
            <div className="absolute top-0 right-12 w-20 h-20 border border-ink-black/3 rounded-full"></div>

            {/* Chat Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-ink-black/5 bg-gradient-to-r from-tea-green/10 to-transparent relative z-10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-tea-green/30 rounded-full flex items-center justify-center text-green-800 font-calligraphy text-lg">
                  馆
                </div>
                <div>
                  <h2 className="font-xiaowei text-base text-ink-black">知识馆长</h2>
                  <p className="text-xs text-charcoal/50 font-serif flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-tea-green rounded-full animate-pulse"></span>
                    在线 · RAG + DeepSeek
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {sessionId && (
                  <span className="text-xs text-charcoal/40 font-serif">
                    会话：{sessionId.slice(-8)}
                  </span>
                )}
                <button
                  onClick={handleClearHistory}
                  className="text-xs text-charcoal/50 hover:text-vermilion transition-colors font-serif flex items-center gap-1 px-2 py-1.5 rounded-sm hover:bg-vermilion/5"
                >
                  <span>🗑️</span>
                  清空
                </button>
              </div>
            </div>

            {/* Messages Container */}
            <div
              ref={messagesContainerRef}
              className="flex-1 overflow-y-auto"
            >
              <div className="p-5 space-y-4">
                {isLoadingHistory ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="flex items-center gap-2 text-charcoal/40 text-xs font-serif">
                      <span className="w-3.5 h-3.5 border-2 border-tea-green border-t-transparent rounded-full animate-spin"></span>
                      加载历史对话...
                    </div>
                  </div>
                ) : (
                  <>
                    {messages.map(msg => (
                      <div
                        key={msg.id}
                        className={`flex items-start gap-3 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}
                      >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                          msg.sender === 'agent'
                            ? 'bg-tea-green/30 text-green-800 font-calligraphy text-base'
                            : 'border border-ink-black/20 overflow-hidden bg-rice-paper'
                        }`}>
                          {msg.sender === 'agent' ? (
                            <span>馆</span>
                          ) : (
                            <img
                              src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                              alt="User"
                              className="w-full h-full"
                            />
                          )}
                        </div>
                        <div className={`max-w-[75%] p-3 rounded-sm shadow-sm ${
                          msg.sender === 'agent'
                            ? 'bg-white border border-ink-black/10 rounded-tl-sm'
                            : 'bg-tea-green text-ink-black rounded-tr-sm'
                        }`}>
                          <div className="markdown-wrapper">
                            <MarkdownContent content={msg.content} />
                          </div>

                          {msg.relatedEntities && msg.relatedEntities.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1.5">
                              {msg.relatedEntities.map((entity, idx) => (
                                <span
                                  key={idx}
                                  className="text-xs bg-tea-green/40 text-charcoal px-1.5 py-0.5 rounded-sm font-serif"
                                >
                                  {entity}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}

                    {loading && (
                      <div className="flex items-center gap-2 text-charcoal/60 text-xs ml-10 font-serif">
                        <span className="w-1.5 h-1.5 bg-charcoal/40 rounded-full animate-bounce"></span>
                        <span className="w-1.5 h-1.5 bg-charcoal/40 rounded-full animate-bounce delay-100"></span>
                        <span className="w-1.5 h-1.5 bg-charcoal/40 rounded-full animate-bounce delay-200"></span>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>

            {/* Follow-up Questions */}
            {followUpQuestions.length > 0 && (
              <div className="px-5 py-3 border-t border-ink-black/5 bg-rice-paper/50">
                <p className="text-xs text-charcoal/50 mb-2 font-serif">您可能还想知道：</p>
                <div className="flex flex-wrap gap-2">
                  {followUpQuestions.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleFollowUpClick(question)}
                      className="text-xs bg-white border border-ink-black/10 text-charcoal px-3 py-1.5 rounded-sm hover:border-tea-green hover:bg-tea-green/10 transition-all font-serif"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t border-ink-black/5 bg-rice-paper/30">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="向知识馆长提问..."
                  className="flex-grow px-3 py-2.5 border border-ink-black/20 rounded-sm focus:outline-none focus:border-vermilion bg-white font-serif text-sm text-charcoal placeholder-charcoal/40"
                />
                <Button
                  onClick={() => handleSend()}
                  disabled={loading}
                  className="px-5 py-2.5 text-sm"
                >
                  {loading ? '发送中...' : '发送'}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default KnowledgeCurator;
