import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import SuEmbroidery from '../assets/Suzhou-embroidery.png';
import PurpleClay from '../assets/Purple-Clay.png';

const MyPractice = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-rice-paper">
      <Navbar />
      
      <main className="pt-32 pb-20 px-4 md:px-12 max-w-7xl mx-auto">
        
        {/* Dashboard Header */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-12 border-b border-ink-black/10 pb-8">
          <div>
            <h1 className="font-calligraphy text-5xl mb-4 text-ink-black">修习之路</h1>
            <p className="text-charcoal/60 font-serif text-lg tracking-widest">路漫漫其修远兮，吾将上下而求索</p>
          </div>
          <div className="text-right mt-6 md:mt-0">
            <div className="text-6xl font-serif text-vermilion">Lv.2</div>
            <div className="text-sm text-charcoal/60 font-sans tracking-widest uppercase">Inheritor Level</div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
          <div className="bg-white p-6 rounded-sm card-shadow text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-ink-black/5 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500"></div>
            <div className="relative z-10">
              <div className="text-4xl font-serif mb-2">12.5h</div>
              <div className="text-xs text-charcoal/60 uppercase tracking-widest">总修习时长</div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-sm card-shadow text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-vermilion/5 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500"></div>
            <div className="relative z-10">
              <div className="text-4xl font-serif mb-2 text-vermilion">85%</div>
              <div className="text-xs text-charcoal/60 uppercase tracking-widest">平均准确率</div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-sm card-shadow text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-cyan-glaze/5 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500"></div>
            <div className="relative z-10">
              <div className="text-4xl font-serif mb-2 text-cyan-glaze">3</div>
              <div className="text-xs text-charcoal/60 uppercase tracking-widest">掌握技法</div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-sm card-shadow text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-tea-green/20 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500"></div>
            <div className="relative z-10">
              <div className="text-4xl font-serif mb-2 text-ink-black/80">15</div>
              <div className="text-xs text-charcoal/60 uppercase tracking-widest">完成作品</div>
            </div>
          </div>
        </div>

        {/* Recent Projects */}
        <h2 className="font-xiaowei text-3xl mb-8 border-l-4 border-vermilion pl-4">正在修习</h2>
        
        <div className="space-y-6 mb-16">
          
          {/* Project Item 1 */}
          <div className="bg-white p-6 rounded-sm card-shadow flex flex-col md:flex-row gap-6 items-center">
            <div className="w-full md:w-32 h-32 bg-gray-200 rounded-sm overflow-hidden flex-shrink-0">
              <img src={SuEmbroidery} className="w-full h-full object-cover" alt="Suzhou Embroidery" />
            </div>
            <div className="flex-grow w-full">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-xiaowei text-2xl text-ink-black">苏绣 · 平针基础</h3>
                  <p className="text-sm text-charcoal/60">上次练习: 10分钟前</p>
                </div>
                <div className="border-2 border-vermilion text-vermilion font-calligraphy px-3 py-1 rounded-sm transform -rotate-2 opacity-80 text-lg">进行中</div>
              </div>
              
              <div className="w-full bg-gray-100 h-2 rounded-full mb-2 overflow-hidden">
                <div className="bg-vermilion h-full w-[75%] rounded-full"></div>
              </div>
              <div className="flex justify-between text-xs text-charcoal/60">
                <span>进度: 75%</span>
                <span>目标: 掌握起针与收针</span>
              </div>
            </div>
            <div className="flex-shrink-0 w-full md:w-auto flex md:flex-col gap-2">
              <Button className="text-sm px-6 py-2" onClick={() => navigate('/vision-mentor?scenario=embroidery')}>继续练习</Button>
              <Button variant="outline" className="text-sm px-6 py-2">查看报告</Button>
            </div>
          </div>

          {/* Project Item 2 */}
          <div className="bg-white p-6 rounded-sm card-shadow flex flex-col md:flex-row gap-6 items-center opacity-70 hover:opacity-100 transition-opacity">
            <div className="w-full md:w-32 h-32 bg-gray-200 rounded-sm overflow-hidden flex-shrink-0">
              <img src={PurpleClay} className="w-full h-full object-cover" alt="Purple Clay" />
            </div>
            <div className="flex-grow w-full">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-xiaowei text-2xl text-ink-black">紫砂 · 拍泥片</h3>
                  <p className="text-sm text-charcoal/60">上次练习: 昨天</p>
                </div>
                <div className="border-2 border-charcoal/40 text-charcoal/40 font-calligraphy px-3 py-1 rounded-sm transform -rotate-2 opacity-80 text-lg">暂停</div>
              </div>
              
              <div className="w-full bg-gray-100 h-2 rounded-full mb-2 overflow-hidden">
                <div className="bg-cyan-glaze h-full w-[30%] rounded-full"></div>
              </div>
              <div className="flex justify-between text-xs text-charcoal/60">
                <span>进度: 30%</span>
                <span>目标: 泥片厚度均匀</span>
              </div>
            </div>
            <div className="flex-shrink-0 w-full md:w-auto flex md:flex-col gap-2">
              <Button className="text-sm px-6 py-2 bg-ink-black hover:bg-cyan-glaze" onClick={() => navigate('/vision-mentor?scenario=clay')}>恢复练习</Button>
            </div>
          </div>

        </div>

        {/* Certificates */}
        <h2 className="font-xiaowei text-3xl mb-8 border-l-4 border-tea-green pl-4">我的证书</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border-4 border-double border-ink-black/10 p-8 bg-rice-paper text-center relative overflow-hidden group cursor-pointer hover:border-vermilion/30 transition-colors">
            <div className="absolute top-0 right-0 w-16 h-16 bg-vermilion/10 rounded-bl-full"></div>
            <div className="font-calligraphy text-4xl mb-4 text-ink-black">结业证书</div>
            <p className="text-sm text-charcoal/60 mb-6 font-serif">兹证明 李明 完成<br />苏绣初级课程修习</p>
            <div className="text-xs text-charcoal/40 font-sans tracking-widest">2026.02.15</div>
            <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity text-vermilion text-sm font-bold">点击下载</div>
          </div>
        </div>

      </main>
    </div>
  );
};

export default MyPractice;
