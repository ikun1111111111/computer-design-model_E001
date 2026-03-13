import React from 'react';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import HomeImage from '../assets/Home.png';

const Home = () => {
  return (
    <div className="min-h-screen bg-rice-paper">
      <Navbar />
      
      {/* Hero Section */}
      <main className="pt-32 pb-20 px-4 md:px-12 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 mb-24">
          {/* Left: Text */}
          <div className="lg:col-span-5 flex flex-col justify-center relative">
            {/* Decorative vertical line */}
            <div className="absolute -left-6 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-vermilion to-transparent opacity-30"></div>

            <div className="inline-block mb-6">
              <span className="seal-border text-vermilion font-calligraphy text-lg">非遗新造</span>
            </div>
            <h1 className="font-calligraphy text-6xl md:text-7xl lg:text-8xl mb-6 leading-tight text-ink-black">
              指尖<br />
              <span className="text-vermilion">乾坤</span>
            </h1>
            <p className="font-serif text-lg md:text-xl text-charcoal leading-loose mb-10 max-w-md">
              以数字之眼，观非遗之美。<br />
              通过 AI 视觉纠偏、知识图谱与风格复原，<br />
              让千年技艺触手可及。
            </p>

            <div className="flex gap-6">
              <Button onClick={() => window.location.href = '/craft-library'}>开始修习</Button>
              <Button variant="outline" onClick={() => window.location.href = '/shadow-puppet'}>皮影戏</Button>
            </div>
          </div>

          {/* Right: Visual */}
          <div className="lg:col-span-7 relative h-[600px] flex items-center justify-center">
            {/* Abstract Circle Background */}
            <div className="absolute w-[500px] h-[500px] rounded-full border border-ink-black/5 animate-spin-slow"></div>
            <div className="absolute w-[400px] h-[400px] rounded-full border border-ink-black/10"></div>

            {/* Main Visual Image */}
            <div className="relative z-10 w-full h-full rounded-lg overflow-hidden shadow-2xl transform rotate-2 hover:rotate-0 transition-transform duration-700">
              <img src={HomeImage} alt="Ink Wash Landscape" className="w-full h-full object-cover filter contrast-110" />
              <div className="absolute inset-0 bg-gradient-to-t from-ink-black/60 to-transparent flex items-end p-8">
                <div className="text-rice-paper">
                  <h3 className="font-calligraphy text-3xl mb-2">皮影戏 · 光影艺术</h3>
                  <p className="font-sans text-sm opacity-80">新增热门修习项目</p>
                </div>
              </div>
            </div>

            {/* Floating Badge */}
            <div className="absolute -right-4 top-20 bg-rice-paper p-4 shadow-xl border-l-4 border-vermilion animate-float z-20 max-w-xs">
              <div className="flex items-start gap-3">
                <div className="text-vermilion text-2xl">❝</div>
                <div>
                  <p className="text-sm font-serif italic text-charcoal">
                    "一口叙说千古事，双手对舞百万兵。皮影戏真的太有魅力了！"
                  </p>
                  <p className="text-xs text-right mt-2 text-charcoal/60">— 学员评价</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Agents Section */}
        <div className="mb-20">
          <div className="flex justify-between items-end mb-12 border-b border-ink-black/10 pb-4">
            <div>
              <h2 className="font-xiaowei text-3xl mb-2">三位导师</h2>
              <p className="font-sans text-charcoal/60 text-sm">Multi-Agent Collaborative System</p>
            </div>
            <div className="hidden md:block text-ink-black/40 font-calligraphy text-2xl">
              师者 · 匠心 · 智识
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Agent 1: Vision */}
            <div className="group card-shadow bg-white p-8 rounded-sm relative overflow-hidden cursor-pointer ink-spread border-t-4 border-cyan-glaze hover:shadow-xl transition-all duration-300">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="font-calligraphy text-9xl">眼</span>
              </div>
              <div className="relative z-10">
                <div className="w-12 h-12 bg-cyan-glaze/10 rounded-full flex items-center justify-center mb-6 text-cyan-glaze">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                </div>
                <h3 className="font-xiaowei text-2xl mb-3 group-hover:text-cyan-glaze transition-colors">视觉导师 Agent</h3>
                <p className="text-charcoal/70 text-sm leading-relaxed mb-6 font-sans">
                  Vision-Mentor
                  <br /><br />
                  实时捕捉手势动作，利用 MediaPipe 与 ST-GCN 技术进行骨骼关键点分析。如同师父在侧，纠正每一针的角度与力度。
                </p>
                <a href="/vision-mentor" className="inline-flex items-center text-cyan-glaze font-bold text-sm tracking-widest hover:underline">
                  进入修习 <span className="ml-2">→</span>
                </a>
              </div>
            </div>

            {/* Agent 2: Knowledge */}
            <div className="group card-shadow bg-white p-8 rounded-sm relative overflow-hidden cursor-pointer ink-spread border-t-4 border-tea-green hover:shadow-xl transition-all duration-300">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="font-calligraphy text-9xl">知</span>
              </div>
              <div className="relative z-10">
                <div className="w-12 h-12 bg-tea-green/30 rounded-full flex items-center justify-center mb-6 text-green-700">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </div>
                <h3 className="font-xiaowei text-2xl mb-3 group-hover:text-green-700 transition-colors">知识馆长 Agent</h3>
                <p className="text-charcoal/70 text-sm leading-relaxed mb-6 font-sans">
                  Knowledge-Curator
                  <br /><br />
                  挂载非遗知识图谱，为您讲述技艺背后的历史与美学。通过 RAG 技术，精准回答每一个关于材料、流派与文化的疑问。
                </p>
                <a href="/knowledge-curator" className="inline-flex items-center text-green-700 font-bold text-sm tracking-widest hover:underline">
                  查阅典籍 <span className="ml-2">→</span>
                </a>
              </div>
            </div>

            {/* Agent 3: Creative */}
            <div className="group card-shadow bg-white p-8 rounded-sm relative overflow-hidden cursor-pointer ink-spread border-t-4 border-vermilion hover:shadow-xl transition-all duration-300">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="font-calligraphy text-9xl">艺</span>
              </div>
              <div className="relative z-10">
                <div className="w-12 h-12 bg-vermilion/10 rounded-full flex items-center justify-center mb-6 text-vermilion">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>
                </div>
                <h3 className="font-xiaowei text-2xl mb-3 group-hover:text-vermilion transition-colors">创意艺匠 Agent</h3>
                <p className="text-charcoal/70 text-sm leading-relaxed mb-6 font-sans">
                  Creative-Artisan
                  <br /><br />
                  将您的草图瞬间转化为非遗风格的大师之作。加载特定 LoRA 模型，探索苏绣质感或青花纹样的无限可能。
                </p>
                <a href="/creative-artisan" className="inline-flex items-center text-vermilion font-bold text-sm tracking-widest hover:underline">
                  开始创作 <span className="ml-2">→</span>
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Shadow Puppet Feature Section */}
        <div className="mb-20">
          <div className="bg-gradient-to-r from-ink-black/90 to-ink-black/70 rounded-sm p-8 md:p-12 relative overflow-hidden text-rice-paper">
            {/* Decorative Background */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute right-0 top-0 w-64 h-64 border border-rice-paper/20 rounded-full"></div>
              <div className="absolute right-32 top-32 w-48 h-48 border border-rice-paper/20 rounded-full"></div>
            </div>

            <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div>
                <div className="inline-block mb-4">
                  <span className="seal-border text-vermilion font-calligraphy text-sm">新增技艺</span>
                </div>
                <h2 className="font-calligraphy text-4xl md:text-5xl mb-6">皮影戏</h2>
                <p className="font-serif text-lg text-rice-paper/80 mb-6 leading-relaxed">
                  一口叙说千古事，双手对舞百万兵。<br />
                  皮影戏起源于西汉，是光影艺术与戏曲表演的完美结合。<br />
                  2011 年入选联合国教科文组织人类非物质文化遗产代表作名录。
                </p>
                <div className="flex flex-wrap gap-4 mb-8">
                  <div className="bg-rice-paper/10 px-4 py-2 rounded-sm">
                    <span className="text-vermilion font-bold">10+</span>
                    <span className="text-rice-paper/70 text-sm ml-2">主要流派</span>
                  </div>
                  <div className="bg-rice-paper/10 px-4 py-2 rounded-sm">
                    <span className="text-vermilion font-bold">9</span>
                    <span className="text-rice-paper/70 text-sm ml-2">制作工艺</span>
                  </div>
                  <div className="bg-rice-paper/10 px-4 py-2 rounded-sm">
                    <span className="text-vermilion font-bold">8</span>
                    <span className="text-rice-paper/70 text-sm ml-2">经典剧目</span>
                  </div>
                </div>
                <Button onClick={() => window.location.href = '/shadow-puppet'}>学习皮影戏</Button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/10 backdrop-blur-sm p-4 rounded-sm">
                  <div className="text-vermilion text-3xl mb-2">影</div>
                  <h3 className="font-xiaowei text-lg mb-2">光影艺术</h3>
                  <p className="text-sm text-rice-paper/70">灯光照射下，影人投影于幕布，展现千古故事</p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm p-4 rounded-sm">
                  <div className="text-cyan-glaze text-3xl mb-2">雕</div>
                  <h3 className="font-xiaowei text-lg mb-2">雕刻工艺</h3>
                  <p className="text-sm text-rice-paper/70">阳刻阴刻结合，镂空技法，精美绝伦</p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm p-4 rounded-sm">
                  <div className="text-tea-green text-3xl mb-2">唱</div>
                  <h3 className="font-xiaowei text-lg mb-2">唱腔音乐</h3>
                  <p className="text-sm text-rice-paper/70">各地流派唱腔独特，乐器伴奏丰富</p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm p-4 rounded-sm">
                  <div className="text-amber-500 text-3xl mb-2">演</div>
                  <h3 className="font-xiaowei text-lg mb-2">操纵技法</h3>
                  <p className="text-sm text-rice-paper/70">三根竹签操纵影人，手势动作精妙</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard Preview */}
        <div className="bg-white rounded-sm p-8 card-shadow relative">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-xiaowei text-2xl">修习档案</h2>
            <span className="text-sm text-gray-400 font-sans">上次更新: 今日 14:30</span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center p-4 border-r border-gray-100 last:border-0">
              <div className="text-4xl font-serif text-ink-black mb-2">12.5</div>
              <div className="text-xs text-charcoal/60 tracking-wider">修习小时</div>
            </div>
            <div className="text-center p-4 border-r border-gray-100 last:border-0">
              <div className="text-4xl font-serif text-vermilion mb-2">85%</div>
              <div className="text-xs text-charcoal/60 tracking-wider">动作准确率</div>
            </div>
            <div className="text-center p-4 border-r border-gray-100 last:border-0">
              <div className="text-4xl font-serif text-cyan-glaze mb-2">3</div>
              <div className="text-xs text-charcoal/60 tracking-wider">掌握技法</div>
            </div>
            <div className="text-center p-4">
              <div className="text-4xl font-serif text-ink-black mb-2">Lv.2</div>
              <div className="text-xs text-charcoal/60 tracking-wider">传承等级</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-ink-black text-rice-paper py-12 border-t-4 border-vermilion">
        <div className="max-w-7xl mx-auto px-4 md:px-12 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-rice-paper text-ink-black flex items-center justify-center font-calligraphy text-2xl rounded-sm">
              承
            </div>
            <div>
              <h4 className="font-xiaowei text-xl">数字传承人</h4>
              <p className="text-xs text-charcoal/60 font-sans">非遗工艺流程交互教学与复原系统</p>
            </div>
          </div>
          <div className="text-charcoal/60 text-sm font-sans text-center md:text-right">
            <p>© 2026 The Digital Inheritor Project.</p>
            <p>Designed for Chinese Collegiate Computing Competition.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
