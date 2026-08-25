import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, X, Sparkles } from 'lucide-react';
import { aiService } from '../../services/aiService';

interface Message {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  steps?: Array<{ action: string; observation: any }>;
}

export const AIAssistantWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'agent',
      text: 'Hello! I am your E-Commerce AI Business Assistant. Ask me about store products, low stock items, sales trends, or executive KPIs!',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const formatAgentText = (value: unknown): string => {
    if (value === null || value === undefined) return '';
    if (typeof value !== 'string') {
      return formatAgentText(JSON.stringify(value));
    }

    const trimmed = value.trim().replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
    if (!trimmed) return '';

    try {
      if (
        (trimmed.startsWith('{') && trimmed.endsWith('}')) ||
        (trimmed.startsWith('[') && trimmed.endsWith(']'))
      ) {
        const parsed = JSON.parse(trimmed);
        if (typeof parsed === 'object' && parsed !== null) {
          if (typeof parsed.final_answer === 'string') return formatAgentText(parsed.final_answer);
          if (typeof parsed.answer === 'string') return formatAgentText(parsed.answer);
          if (typeof parsed.message === 'string') return formatAgentText(parsed.message);

          return Object.entries(parsed).map(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
            const displayValue = typeof value === 'object' ? formatAgentText(value) : String(value);
            return `• ${label}: ${displayValue}`;
          }).join('\n');
        }
      }
    } catch {
      // Not JSON
    }

    return value;
  };

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userText = input.trim();
    setInput('');
    const userMsgId = Date.now().toString();

    setMessages((prev) => [...prev, { id: userMsgId, sender: 'user', text: userText }]);
    setIsLoading(true);

    try {
      const res = await aiService.queryAgent(userText);
      const rawAnswer = res.data?.final_answer || 'Processed request successfully.';
      const cleanAnswer = formatAgentText(rawAnswer);

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'agent',
          text: cleanAnswer,
          steps: res.data?.steps,
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'agent',
          text: `Error: ${err.message || 'Failed to connect to AI Agent Service.'}`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 990 }}>
      {/* Floating Trigger Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="glow-pulse"
          style={{
            width: '56px',
            height: '56px',
            borderRadius: 'var(--radius-full)',
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-glow)',
          }}
        >
          <Bot size={26} />
        </button>
      )}

      {/* Chatbot Window */}
      {isOpen && (
        <div
          className="glass-panel animate-fade-in"
          style={{
            width: '400px',
            height: '540px',
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 20px 40px rgba(0, 0, 0, 0.5)',
            border: '1px solid var(--border-glow)',
          }}
        >
          {/* Header */}
          <div
            style={{
              padding: '1rem 1.25rem',
              borderBottom: '1px solid var(--border-color)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'rgba(99, 102, 241, 0.1)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
              <div style={{ padding: '0.4rem', borderRadius: 'var(--radius-md)', background: 'var(--accent-primary)', color: '#fff' }}>
                <Sparkles size={18} />
              </div>
              <div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700 }}>AI Business Assistant</h4>
                <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>Autonomous ReAct Agent</span>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} style={{ background: 'transparent', color: 'var(--text-muted)' }}>
              <X size={20} />
            </button>
          </div>

          {/* Messages Body */}
          <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {messages.map((msg) => (
              <div
                key={msg.id}
                style={{
                  display: 'flex',
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <div
                  style={{
                    maxWidth: '85%',
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    fontSize: '0.85rem',
                    lineHeight: 1.5,
                    whiteSpace: 'pre-wrap',
                    background: msg.sender === 'user' ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.08)',
                    color: '#fff',
                    border: msg.sender === 'user' ? 'none' : '1px solid var(--border-color)',
                  }}
                >
                  {msg.text}
                  {msg.steps && msg.steps.length > 0 && (
                    <div style={{ marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid rgba(255,255,255,0.1)', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                      <strong>Tool Actions Executed:</strong>
                      <ul style={{ paddingLeft: '1rem', marginTop: '0.25rem' }}>
                        {msg.steps.map((s, idx) => (
                          <li key={idx}>⚙️ {s.action}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                AI Agent is reasoning and executing tools...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form
            onSubmit={handleSend}
            style={{
              padding: '0.85rem',
              borderTop: '1px solid var(--border-color)',
              display: 'flex',
              gap: '0.5rem',
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AI Agent (e.g. show sales KPIs)..."
              style={{
                flex: 1,
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-md)',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                outline: 'none',
                fontSize: '0.85rem',
              }}
            />
            <button
              type="submit"
              disabled={isLoading}
              style={{
                padding: '0.65rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--accent-primary)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
