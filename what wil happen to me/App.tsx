
import React, { useState, useEffect, useRef } from 'react';
import { Stage, PresetData, Role, Message } from './types';
import { ROLES, PRESET_OPTIONS, INITIAL_QUESTIONS } from './constants';
import { getRoleResponse, getSurvivalSummary, generateFollowupOptions } from './services/geminiService';
import ParticleBackground from './components/ParticleBackground';
import TypewriterText from './components/TypewriterText';

const App: React.FC = () => {
  const [stage, setStage] = useState<Stage>('START');
  const [preset, setPreset] = useState<PresetData>({
    jumpHeight: PRESET_OPTIONS.jumpHeight[0],
    balloonSize: PRESET_OPTIONS.balloonSize[0],
    heliumRate: PRESET_OPTIONS.heliumRate[0],
    weight: PRESET_OPTIONS.weight[0],
    landingScene: PRESET_OPTIONS.landingScene[0]
  });
  
  // 存储用户手动输入的预设
  const [customPresets, setCustomPresets] = useState<Record<string, string>>({
    jumpHeight: '',
    balloonSize: '',
    heliumRate: '',
    weight: '',
    landingScene: ''
  });

  const [userQuestion, setUserQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [currentSpeakerIndex, setCurrentSpeakerIndex] = useState(-1);
  const [summaryResult, setSummaryResult] = useState<{ summary: string; status: '生存' | '死亡' } | null>(null);
  const [followupOptions, setFollowupOptions] = useState<string[]>([]);
  const [selectedRoleHistory, setSelectedRoleHistory] = useState<Role | null>(null);
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // 综合计算最终预设
  const finalPreset = {
    jumpHeight: customPresets.jumpHeight.trim() || preset.jumpHeight,
    balloonSize: customPresets.balloonSize.trim() || preset.balloonSize,
    heliumRate: customPresets.heliumRate.trim() || preset.heliumRate,
    weight: customPresets.weight.trim() || preset.weight,
    landingScene: customPresets.landingScene.trim() || preset.landingScene,
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, currentSpeakerIndex]);

  const startDiscussion = async (question: string) => {
    if (!question.trim()) return;
    setUserQuestion(question);
    setMessages([]);
    setFollowupOptions([]);
    setSummaryResult(null);
    setStage('IN_CALL');
    setIsAiThinking(true);

    let discussionHistory = "";
    const newMessages: Message[] = [];

    for (let i = 0; i < ROLES.length; i++) {
      setCurrentSpeakerIndex(i);
      const role = ROLES[i];
      const answer = await getRoleResponse(role, question, finalPreset as PresetData, discussionHistory);
      const msg: Message = { roleId: role.id, content: answer, timestamp: Date.now() };
      newMessages.push(msg);
      setMessages([...newMessages]);
      discussionHistory += `\n${role.name}: ${answer}`;
      await new Promise(r => setTimeout(r, 2500));
    }

    setCurrentSpeakerIndex(-1);
    setIsAiThinking(false);

    const summary = await getSurvivalSummary(question, discussionHistory, finalPreset as PresetData);
    setSummaryResult(summary);

    const followups = await generateFollowupOptions(question, discussionHistory);
    setFollowupOptions(followups);
  };

  const handleAcceptCall = () => {
    setStage('CONNECTING');
    setTimeout(() => {
      setStage('IN_CALL');
    }, 2500);
  };

  const resetApp = () => {
    setStage('START');
    setMessages([]);
    setSummaryResult(null);
    setUserQuestion('');
    setFollowupOptions([]);
    setCurrentSpeakerIndex(-1);
    setIsAiThinking(false);
    setSelectedRoleHistory(null);
    setCustomPresets({
      jumpHeight: '', balloonSize: '', heliumRate: '', weight: '', landingScene: ''
    });
  };

  const renderStart = () => (
    <div className="relative z-10 flex flex-col items-center justify-center min-h-screen text-center animate-in fade-in duration-1000 px-6">
      <h1 className="text-5xl md:text-8xl font-black mb-6 title-gradient tracking-tighter drop-shadow-2xl">What will happen to me</h1>
      <p className="text-xl text-indigo-400 font-medium mb-12 max-w-lg italic opacity-90 drop-shadow-lg">
        一场关于氦气、气球与万米高空的终极命题讨论
      </p>
      <button 
        onClick={() => setStage('PRESET')}
        className="px-14 py-5 btn-metal text-white rounded-full text-2xl font-black active:scale-95 flex items-center gap-4"
      >
        开启议程
      </button>
    </div>
  );

  const renderPreset = () => (
    <div className="relative z-10 flex items-center justify-center min-h-screen p-4 animate-in slide-in-from-bottom-8 duration-700">
      <div className="glass-premium w-full max-w-3xl rounded-[40px] p-8 md:p-10 flex flex-col overflow-hidden max-h-[90vh] shadow-2xl">
        <div className="mb-6 flex justify-between items-end border-b border-indigo-100/30 pb-4">
          <div>
            <h2 className="text-3xl font-black text-indigo-900 tracking-tight">实验环境配置</h2>
            <p className="text-indigo-400 text-sm font-medium mt-1">设置场景参数或手动输入你的设想</p>
          </div>
          <span className="text-xs font-black text-indigo-300 uppercase tracking-widest bg-white/40 px-3 py-1 rounded-full">Phase 01</span>
        </div>
        
        <div className="flex-1 overflow-y-auto hide-scrollbar space-y-6 pr-2">
          {(Object.keys(PRESET_OPTIONS) as Array<keyof typeof PRESET_OPTIONS>).map((key) => {
            const labelMap: Record<string, string> = {
              jumpHeight: '跳下高度',
              balloonSize: '气球大小',
              heliumRate: '充气速度',
              weight: '你的体重',
              landingScene: '下方场景'
            };
            return (
              <div key={key} className="p-5 bg-white/20 rounded-3xl border border-white/40 shadow-sm transition-all hover:bg-white/30">
                <label className="text-xs font-black text-indigo-800/40 mb-3 block uppercase tracking-wider">{labelMap[key]}</label>
                <div className="flex flex-wrap gap-2 mb-3">
                  {PRESET_OPTIONS[key].map(opt => (
                    <button
                      key={opt}
                      onClick={() => setPreset(prev => ({ ...prev, [key]: opt }))}
                      className={`px-4 py-2 rounded-xl text-xs font-black transition-all btn-metal-small ${
                        preset[key] === opt ? 'active' : ''
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
                <input 
                  type="text"
                  placeholder={`或输入自定义${labelMap[key]}...`}
                  value={customPresets[key]}
                  onChange={(e) => setCustomPresets(prev => ({ ...prev, [key]: e.target.value }))}
                  className="w-full bg-white/40 border border-white/60 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400/20 transition-all text-indigo-950 font-bold placeholder:text-indigo-300/60"
                />
              </div>
            );
          })}
        </div>

        <div className="mt-6 pt-4 border-t border-indigo-100/30 flex justify-end">
          <button 
            onClick={() => setStage('CALLING')}
            className="px-12 py-4 btn-metal text-white rounded-[24px] font-black text-xl shadow-2xl active:scale-95"
          >
            连线议会
          </button>
        </div>
      </div>
    </div>
  );

  const renderCalling = () => (
    <div className="relative z-10 flex flex-col items-center justify-center min-h-screen bg-indigo-950/20 backdrop-blur-md animate-in fade-in duration-500">
      <div className="flex flex-col items-center">
        <div className="grid grid-cols-2 gap-10 mb-20">
          {ROLES.map((r, i) => (
            <div key={r.id} className="relative group animate-pulse" style={{ animationDelay: `${i * 0.3}s` }}>
              <img src={r.avatar} className="w-28 h-28 md:w-36 md:h-36 rounded-full border-[8px] border-white/30 shadow-2xl" />
              <div className="absolute inset-0 rounded-full ring-[12px] ring-indigo-400/20 animate-ping opacity-30" />
            </div>
          ))}
        </div>
        <h2 className="text-white text-4xl md:text-6xl font-black tracking-[0.4em] mb-6 drop-shadow-2xl">议会连线中</h2>
        <p className="text-indigo-100/60 text-xl font-light tracking-widest italic animate-bounce">专家团正在加入加密频道...</p>
      </div>
      <div className="absolute bottom-24 flex gap-24">
        <button 
          onClick={resetApp}
          className="w-24 h-24 bg-red-500 rounded-full flex items-center justify-center shadow-2xl hover:scale-110 active:scale-90 transition-all group border-4 border-white/20"
        >
          <svg className="w-12 h-12 text-white rotate-[135deg]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.288 1.209L8.13 10.13a13.045 13.045 0 005.741 5.741l1.758-1.758a1 1 0 011.209-.288l4.493 1.498a1 1 0 01.684.948V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </button>
        <button 
          onClick={handleAcceptCall}
          className="w-24 h-24 bg-green-500 rounded-full flex items-center justify-center shadow-2xl hover:scale-110 active:scale-90 transition-all animate-bounce border-4 border-white/20"
        >
          <svg className="w-12 h-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.288 1.209L8.13 10.13a13.045 13.045 0 005.741 5.741l1.758-1.758a1 1 0 011.209-.288l4.493 1.498a1 1 0 01.684.948V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
        </button>
      </div>
    </div>
  );

  const renderConnecting = () => (
    <div className="relative z-10 flex flex-col items-center justify-center min-h-screen bg-indigo-900/30 backdrop-blur-xl animate-in fade-in duration-500">
      <div className="loader-ring mb-10"></div>
      <h2 className="text-white text-3xl font-black tracking-widest mb-8 drop-shadow-lg">正在同步加密数据</h2>
      
      <div className="w-80 h-4 bg-white/10 rounded-full overflow-hidden mb-6 border border-white/10 shadow-inner">
        <div className="h-full progress-fill" />
      </div>
      
      <p className="text-indigo-200/50 text-xs uppercase font-black tracking-widest">Protocol V4.2 Establishing Connection...</p>
    </div>
  );

  const renderInCall = () => (
    <div className="relative z-10 flex flex-col h-screen overflow-hidden text-indigo-950 animate-in fade-in duration-1000">
      {/* 状态栏 */}
      <div className="glass-premium h-16 flex items-center justify-between px-8 shrink-0 shadow-lg border-b border-white/20">
        <div className="flex items-center gap-5">
          <div className="relative flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-4 w-4 bg-green-500 shadow-sm border-2 border-white"></span>
          </div>
          <span className="font-black text-2xl tracking-tighter text-indigo-900">AI 议会现场讨论</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="glass-dark-premium px-5 py-1.5 rounded-full text-[11px] font-black text-white uppercase tracking-wider shadow-md border border-white/10">
            {finalPreset.jumpHeight} · {finalPreset.landingScene}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-hidden p-6 relative flex flex-col lg:flex-row gap-8">
        {/* 角色视频网格 */}
        <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-8 h-full">
          {ROLES.map((role, idx) => {
            const isSpeaking = currentSpeakerIndex === idx;
            const lastMsg = messages.find(m => m.roleId === role.id && messages.indexOf(m) === messages.length - 1);
            return (
              <div key={role.id} className="relative group h-full">
                <div className={`glass-premium h-full rounded-[48px] flex flex-col items-center justify-center transition-all duration-700 overflow-hidden border-4 shadow-2xl ${
                  isSpeaking ? 'speaker-active bg-white/80 ring-8 ring-amber-400/20' : 'hover:bg-white/50 border-white/30'
                }`}>
                  <div 
                    onClick={() => setSelectedRoleHistory(role)}
                    className={`w-28 h-28 md:w-40 md:h-40 rounded-full overflow-hidden border-[8px] border-white shadow-2xl cursor-pointer transition-all duration-500 active:scale-95 ${
                      isSpeaking ? 'ring-8 ring-amber-400/40 animate-pulse' : ''
                    }`}
                  >
                    <img src={role.avatar} className="w-full h-full object-cover" />
                  </div>
                  
                  <div className="mt-6 text-center">
                    <span className="block font-black text-2xl md:text-3xl tracking-tight text-indigo-950">{role.name}</span>
                    <span className="text-xs font-black uppercase tracking-[0.25em] text-indigo-400 mt-2 block opacity-70">{role.title}</span>
                  </div>
                  
                  {isSpeaking && lastMsg && (
                    <div className="absolute inset-x-6 bottom-6 glass-dark-premium p-6 rounded-[32px] border border-white/20 text-white font-black text-base leading-relaxed shadow-2xl max-h-[45%] flex flex-col">
                      <div className="overflow-y-auto hide-scrollbar pr-2 scroll-smooth">
                        <TypewriterText text={lastMsg.content} speed={25} />
                        <span className="type-cursor" />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* 侧边信息栏 & 控制台 */}
        <div className="w-full lg:w-[420px] shrink-0 flex flex-col gap-8 h-full">
          {/* 实时笔录 */}
          <div className="glass-premium flex-1 rounded-[48px] p-8 flex flex-col overflow-hidden shadow-2xl border-white/40">
             <div className="flex items-center justify-between mb-6 px-1">
                <h3 className="font-black text-indigo-900 text-xl tracking-tight">核心议程笔录</h3>
                <span className="text-[10px] font-black text-indigo-400 bg-white/70 px-4 py-1.5 rounded-full shadow-inner border border-white/50 uppercase tracking-widest">LIVE STREAM</span>
             </div>
             
             <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-8 pr-3 hide-scrollbar scroll-smooth">
                {messages.length === 0 && !isAiThinking && (
                  <div className="h-full flex flex-col items-center justify-center text-center opacity-40 italic py-24 grayscale">
                    <div className="text-7xl mb-6 animate-bounce">🎙️</div>
                    <p className="text-2xl font-black text-indigo-900/40">等待开启议题</p>
                  </div>
                )}
                
                {messages.map((msg, i) => {
                  const role = ROLES.find(r => r.id === msg.roleId);
                  return (
                    <div key={i} className="flex flex-col gap-3 animate-in slide-in-from-bottom-4 duration-500">
                      <div className="flex items-center gap-3 ml-2">
                        <div className={`w-3 h-3 rounded-full ${role?.color} shadow-lg ring-2 ring-white`} />
                        <span className="text-xs font-black text-indigo-950/50 uppercase tracking-tighter">{role?.name}</span>
                      </div>
                      <div className="bg-white/80 backdrop-blur-2xl p-5 rounded-[28px] rounded-tl-none text-sm leading-relaxed border border-white/90 shadow-lg text-indigo-950 font-black">
                        {msg.content}
                      </div>
                    </div>
                  );
                })}
                
                {isAiThinking && currentSpeakerIndex !== -1 && (
                   <div className="flex items-center gap-4 text-sm text-indigo-600 font-black py-6 px-3 italic animate-pulse">
                      <span className="w-2 h-2 rounded-full bg-indigo-600 animate-ping"></span>
                      {ROLES[currentSpeakerIndex].name} 正在深度解析...
                   </div>
                )}
             </div>
          </div>

          {/* 交互区 */}
          <div className="glass-premium rounded-[40px] p-8 flex flex-col gap-6 shadow-2xl border-white/40">
             <div className="flex gap-3">
                <input 
                   value={userQuestion}
                   onChange={(e) => setUserQuestion(e.target.value)}
                   onKeyDown={(e) => e.key === 'Enter' && startDiscussion(userQuestion)}
                   placeholder="输入你的疯狂设想..."
                   className="flex-1 bg-white/80 border border-white/50 rounded-2xl px-5 py-4 text-base focus:outline-none focus:ring-4 focus:ring-indigo-600/10 transition-all font-black text-indigo-950 placeholder:text-indigo-200"
                />
                <button 
                  disabled={isAiThinking}
                  onClick={() => startDiscussion(userQuestion)}
                  className={`w-14 h-14 flex items-center justify-center rounded-2xl transition-all btn-metal text-white ${isAiThinking ? 'opacity-40 grayscale pointer-events-none' : ''}`}
                >
                  <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
             </div>
             
             <div className="flex flex-wrap gap-2.5">
                {(followupOptions.length > 0 ? followupOptions : INITIAL_QUESTIONS).map((q, i) => (
                   <button 
                      key={i}
                      onClick={() => startDiscussion(q)}
                      disabled={isAiThinking}
                      className="text-[11px] font-black px-4 py-2.5 btn-metal-small rounded-2xl transition-all hover:scale-105 active:scale-95 disabled:opacity-40 shadow-sm"
                   >
                      {q}
                   </button>
                ))}
             </div>
          </div>
        </div>
      </div>

      {/* 角色历史弹窗 */}
      {selectedRoleHistory && (
        <div 
          className="fixed inset-0 z-[120] flex items-center justify-center p-8 bg-indigo-950/30 backdrop-blur-3xl animate-in fade-in zoom-in-95 duration-500"
          onClick={() => setSelectedRoleHistory(null)}
        >
           <div 
             className="relative glass-premium max-w-3xl w-full rounded-[64px] overflow-hidden flex flex-col shadow-2xl border-white"
             onClick={(e) => e.stopPropagation()}
           >
              <div className="p-10 flex items-center justify-between border-b border-indigo-100/30 bg-white/30">
                 <div className="flex items-center gap-6">
                    <img src={selectedRoleHistory.avatar} className="w-20 h-20 rounded-full border-4 border-white shadow-2xl" />
                    <div>
                       <h3 className="text-3xl font-black text-indigo-950 tracking-tight">{selectedRoleHistory.name}</h3>
                       <p className="text-sm font-black text-indigo-500 uppercase tracking-widest opacity-70">{selectedRoleHistory.title}</p>
                    </div>
                 </div>
                 <button onClick={() => setSelectedRoleHistory(null)} className="w-14 h-14 flex items-center justify-center bg-white/60 hover:bg-white rounded-full transition-all text-indigo-950 shadow-inner group">
                    <svg className="w-8 h-8 group-hover:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" /></svg>
                 </button>
              </div>
              <div className="p-10 overflow-y-auto max-h-[55vh] space-y-8 hide-scrollbar">
                 {messages.filter(m => m.roleId === selectedRoleHistory.id).map((m, i) => (
                    <div key={i} className="p-8 bg-white/80 rounded-[40px] rounded-tl-none border border-white shadow-xl text-indigo-950 font-black leading-relaxed italic text-xl">
                       “{m.content}”
                    </div>
                 ))}
                 {messages.filter(m => m.roleId === selectedRoleHistory.id).length === 0 && <p className="text-center text-indigo-300 italic text-lg py-10 opacity-60">该专家团成员暂未在连线中发言</p>}
              </div>
           </div>
        </div>
      )}

      {/* 结论弹出层 */}
      {summaryResult && (
        <div className="fixed inset-0 z-[150] flex items-center justify-center p-8 bg-indigo-950/50 backdrop-blur-2xl animate-in fade-in zoom-in-95 duration-700">
           <div className={`relative max-w-xl w-full rounded-[64px] p-12 text-center shadow-2xl border-[8px] transition-all duration-700 ${
               summaryResult.status === '生存' ? 'bg-gradient-to-br from-yellow-50 to-white border-white shadow-amber-200/50' : 'bg-gradient-to-br from-indigo-50 to-white border-white/60 shadow-purple-900/40'
             }`}>
              <div className="text-9xl mb-10 transform scale-125 drop-shadow-2xl">
                {summaryResult.status === '生存' ? '🪂' : '☄️'}
              </div>
              <h2 className={`text-7xl font-black mb-8 tracking-tighter drop-shadow-xl ${summaryResult.status === '生存' ? 'text-amber-500' : 'text-purple-900'}`}>
                {summaryResult.status === '生存' ? '侥幸生存！' : '彻底凉凉！'}
              </h2>
              <div className="bg-white/70 p-10 rounded-[48px] mb-10 border border-white/90 text-indigo-950 leading-relaxed font-black italic text-2xl shadow-inner">
                “{summaryResult.summary}”
              </div>
              <div className="flex gap-6 justify-center">
                 <button onClick={() => setSummaryResult(null)} className="px-10 py-5 btn-metal-small active rounded-[24px] font-black text-lg transition-all active:scale-95 shadow-lg">
                   继续深度议案
                 </button>
                 <button onClick={resetApp} className="px-10 py-5 btn-metal text-white rounded-[24px] font-black text-lg active:scale-95 shadow-2xl">
                   重新开始挑战
                 </button>
              </div>
           </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen w-full relative overflow-hidden bg-white/10">
      <ParticleBackground />
      {/* 动态氛围层 - 降低透明度让粒子更突出 */}
      <div className="fixed inset-0 pointer-events-none bg-gradient-to-br from-purple-400/5 via-transparent to-yellow-400/10 z-0" />
      
      {stage === 'START' && renderStart()}
      {stage === 'PRESET' && renderPreset()}
      {stage === 'CALLING' && renderCalling()}
      {stage === 'CONNECTING' && renderConnecting()}
      {stage === 'IN_CALL' && renderInCall()}
    </div>
  );
};

export default App;
