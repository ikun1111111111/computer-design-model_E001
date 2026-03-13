import React from 'react';

const Navbar = () => {
  return (
    <nav className="fixed w-full z-50 px-8 py-6 flex justify-between items-center backdrop-blur-sm bg-rice-paper/80 border-b border-ink-black/5">
      <a href="/" className="flex items-center gap-4 group">
        <div className="w-10 h-10 border-2 border-ink-black rounded-full flex items-center justify-center font-calligraphy text-xl bg-ink-black text-rice-paper group-hover:bg-vermilion group-hover:border-vermilion transition-colors">
          承
        </div>
        <div className="flex flex-col">
          <span className="font-xiaowei text-lg tracking-widest text-ink-black">数字传承人</span>
          <span className="text-xs uppercase tracking-[0.2em] text-charcoal/60 font-sans">The Digital Inheritor</span>
        </div>
      </a>
      <div className="hidden md:flex gap-12 font-xiaowei text-ink-black/80">
        <a href="/craft-library" className="hover:text-vermilion transition-colors">技艺库</a>
        <a href="/master-workshop" className="hover:text-vermilion transition-colors">大师坊</a>
        <a href="/my-practice" className="hover:text-vermilion transition-colors">我的修习</a>
        <a href="/knowledge-curator" className="hover:text-vermilion transition-colors">知识馆长</a>
      </div>
      <div className="flex items-center gap-4">
        <div className="text-right hidden sm:block">
          <div className="text-sm font-bold">李明</div>
          <div className="text-xs text-charcoal/60">初级学徒</div>
        </div>
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" className="w-10 h-10 rounded-full border border-ink-black/20" />
      </div>
    </nav>
  );
};

export default Navbar;
