import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import EmbroideryMaster from '../assets/Embroidery-Master.png';
import CeramicMaster from '../assets/Ceramic-Master.png';

const MasterWorkshop = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-rice-paper">
      <Navbar />
      
      <main className="pt-32 pb-20 px-4 md:px-12 max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-16 text-center">
          <h1 className="font-calligraphy text-5xl mb-4 text-ink-black">大师工坊</h1>
          <p className="text-charcoal/60 font-serif text-lg tracking-widest">与非遗传承人跨时空对话，汲取匠心智慧</p>
        </div>

        {/* Featured Masters */}
        <div className="space-y-20">
          
          {/* Master 1 */}
          <div className="flex flex-col md:flex-row gap-8 items-center bg-white p-8 rounded-sm card-shadow relative overflow-hidden group hover:shadow-2xl transition-all duration-500">
            <div className="absolute -right-10 -top-10 text-[200px] text-gray-100 font-calligraphy z-0 pointer-events-none select-none">绣</div>
            
            <div className="w-full md:w-1/3 relative z-10">
              <div className="aspect-[3/4] overflow-hidden rounded-sm relative group-hover:shadow-lg transition-shadow">
                <img src={EmbroideryMaster} alt="Lin Huiyin" className="w-full h-full object-cover filter grayscale group-hover:grayscale-0 transition-all duration-700" />
                <div className="absolute bottom-4 left-4 bg-rice-paper/90 backdrop-blur px-4 py-2 border-l-4 border-vermilion">
                  <h3 className="font-xiaowei text-2xl">林徽音</h3>
                  <p className="text-xs text-charcoal/60">国家级苏绣传承人</p>
                </div>
              </div>
            </div>
            
            <div className="w-full md:w-2/3 relative z-10 pl-0 md:pl-8">
              <div className="mb-6">
                <h2 className="font-calligraphy text-4xl mb-4">以针为笔，以线为墨</h2>
                <p className="font-serif text-charcoal leading-loose text-lg">
                  “刺绣不仅仅是技艺，更是修心。每一针的起落，都藏着绣娘的心境。在这里，我将通过数字分身，手把手教你如何运针，如何配色，如何赋予丝线生命。”
                </p>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="bg-rice-paper p-4 border border-ink-black/5">
                  <div className="text-vermilion font-bold text-xl mb-1">50+</div>
                  <div className="text-xs text-charcoal/60">经典针法数据</div>
                </div>
                <div className="bg-rice-paper p-4 border border-ink-black/5">
                  <div className="text-ink-black font-bold text-xl mb-1">24h</div>
                  <div className="text-xs text-charcoal/60">AI 实时陪练</div>
                </div>
              </div>

              <div className="flex gap-4">
                <Button onClick={() => navigate('/vision-mentor?scenario=embroidery')}>拜师学艺</Button>
                <Button variant="outline">查看作品集</Button>
              </div>
            </div>
          </div>

          {/* Master 2 */}
          <div className="flex flex-col md:flex-row-reverse gap-8 items-center bg-white p-8 rounded-sm card-shadow relative overflow-hidden group hover:shadow-2xl transition-all duration-500">
            <div className="absolute -left-10 -top-10 text-[200px] text-gray-100 font-calligraphy z-0 pointer-events-none select-none">陶</div>
            
            <div className="w-full md:w-1/3 relative z-10">
              <div className="aspect-[3/4] overflow-hidden rounded-sm relative group-hover:shadow-lg transition-shadow">
                <img src={CeramicMaster} alt="Chen Mansheng" className="w-full h-full object-cover filter grayscale group-hover:grayscale-0 transition-all duration-700" />
                <div className="absolute bottom-4 right-4 bg-rice-paper/90 backdrop-blur px-4 py-2 border-r-4 border-cyan-glaze text-right">
                  <h3 className="font-xiaowei text-2xl">陈曼生</h3>
                  <p className="text-xs text-charcoal/60">紫砂壶艺大师</p>
                </div>
              </div>
            </div>
            
            <div className="w-full md:w-2/3 relative z-10 pr-0 md:pr-8 text-right md:text-left">
              <div className="mb-6 md:text-right">
                <h2 className="font-calligraphy text-4xl mb-4">方非一式，圆不一相</h2>
                <p className="font-serif text-charcoal leading-loose text-lg">
                  “紫砂的灵魂在于泥料与火候的对话。通过动作捕捉技术，我记录下了拍打泥片时最微妙的力道变化。愿你能通过屏幕，感受到这份指尖的温度。”
                </p>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-8 md:ml-auto md:w-2/3">
                <div className="bg-rice-paper p-4 border border-ink-black/5 text-center">
                  <div className="text-cyan-glaze font-bold text-xl mb-1">100%</div>
                  <div className="text-xs text-charcoal/60">动作还原度</div>
                </div>
                <div className="bg-rice-paper p-4 border border-ink-black/5 text-center">
                  <div className="text-ink-black font-bold text-xl mb-1">3D</div>
                  <div className="text-xs text-charcoal/60">全景烧制模拟</div>
                </div>
              </div>

              <div className="flex gap-4 justify-end md:justify-end">
                <Button className="hover:bg-cyan-glaze" onClick={() => navigate('/vision-mentor?scenario=clay')}>拜师学艺</Button>
                <Button variant="outline">查看作品集</Button>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
};

export default MasterWorkshop;
