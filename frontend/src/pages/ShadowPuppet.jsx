import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import Card from '../components/Card';
import HandTracking from '../components/HandTracking';

const ShadowPuppet = () => {
  const [currentTechnique, setCurrentTechnique] = useState(null);
  const [isPracticing, setIsPracticing] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [score, setScore] = useState(0);
  const videoRef = useRef(null);

  // 皮影戏操纵技法数据
  const techniques = [
    {
      id: 1,
      name: "基本手势",
      difficulty: "入门",
      description: "学习用三根竹签操纵影人的基本手势，一根在颈部控制身体，两根在双手控制手臂动作。",
      steps: [
        "右手持主签（颈部），拇指与食指捏住签杆",
        "左手持手签（双手），中指与无名指夹住签杆",
        "保持手腕放松，手臂自然下垂",
        "练习上下移动主签，观察影人动作"
      ],
      image: "https://images.unsplash.com/photo-1534958156884-4f36b9a9690d?w=400"
    },
    {
      id: 2,
      name: "行走动作",
      difficulty: "初级",
      description: "通过交替移动身体签和手部签，模拟人物行走姿态。",
      steps: [
        "主签轻微上下摆动，模拟身体起伏",
        "左手交替移动两根手签",
        "保持节奏均匀，动作连贯",
        "注意影人双脚与地面的接触感"
      ],
      image: "https://images.unsplash.com/photo-1534958156884-4f36b9a9690d?w=400"
    },
    {
      id: 3,
      name: "武打动作",
      difficulty: "进阶",
      description: "快速挥舞影人，配合翻、滚、跌、扑等动作，展现武打场面。",
      steps: [
        "双手协调配合，主签快速移动",
        "练习翻转手腕，实现影人翻身",
        "掌握力度，避免签子缠绕",
        "配合锣鼓点进行节奏训练"
      ],
      image: "https://images.unsplash.com/photo-1534958156884-4f36b9a9690d?w=400"
    },
    {
      id: 4,
      name: "表情变化",
      difficulty: "进阶",
      description: "通过微调影人角度和距离，表现喜怒哀乐等情绪。",
      steps: [
        "学习调整影人与影窗的距离",
        "练习微调头部角度",
        "掌握侧身、低头、仰头等动作",
        "配合唱腔表达情感"
      ],
      image: "https://images.unsplash.com/photo-1534958156884-4f36b9a9690d?w=400"
    }
  ];

  // 皮影戏知识卡片
  const knowledgeCards = [
    {
      title: "皮影戏起源",
      content: "皮影戏起源于西汉时期（约公元前 2 世纪），发源地为陕西省华县。相传汉武帝爱妃李夫人病逝，方士李少翁用棉帛裁成李夫人影像，涂上色彩，在灯光下投影于帐幕，这被认为是皮影戏的雏形。",
      icon: "历"
    },
    {
      title: "制作工艺",
      content: "皮影制作需要经过选皮、制皮、画稿、过稿、雕刻、上色、上油、组装等 9 道工序。皮质要求薄厚均匀，雕刻技法有阳刻和阴刻两种，色彩鲜艳透明。",
      icon: "工"
    },
    {
      title: "主要流派",
      content: "皮影戏遍布中国大部分地区，形成了陕西皮影、唐山皮影、山东皮影、四川皮影等十大流派，各有独特的艺术风格和唱腔特色。",
      icon: "派"
    },
    {
      title: "文化价值",
      content: "2006 年皮影戏列入国家级非物质文化遗产，2011 年入选联合国教科文组织人类非物质文化遗产代表作名录，被誉为'中国灯影'。",
      icon: "誉"
    }
  ];

  const handlePractice = (technique) => {
    setCurrentTechnique(technique);
    setIsPracticing(true);
    setFeedback(null);
    setScore(0);
  };

  const handleStopPractice = () => {
    setIsPracticing(false);
    setCurrentTechnique(null);
    // 模拟反馈
    setFeedback({
      correctness: 85,
      suggestions: [
        "手腕可以更放松一些",
        "主签移动速度稍微慢一点会更流畅",
        "注意保持身体姿势端正"
      ]
    });
    setScore(85);
  };

  return (
    <div className="min-h-screen bg-rice-paper">
      <Navbar />

      <main className="pt-32 pb-20 px-4 md:px-12 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <div className="inline-block mb-4">
            <span className="seal-border text-vermilion font-calligraphy text-lg">光影艺术</span>
          </div>
          <h1 className="font-calligraphy text-5xl md:text-6xl mb-4 text-ink-black">
            皮影戏 · 操纵技法
          </h1>
          <p className="font-serif text-lg text-charcoal/70 max-w-2xl mx-auto">
            一口叙说千古事，双手对舞百万兵
          </p>
        </div>

        {/* Knowledge Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {knowledgeCards.map((card, index) => (
            <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-vermilion/10 rounded-full flex items-center justify-center mb-4 text-vermilion">
                <span className="font-calligraphy text-2xl">{card.icon}</span>
              </div>
              <h3 className="font-xiaowei text-xl mb-3">{card.title}</h3>
              <p className="text-charcoal/70 text-sm leading-relaxed">{card.content}</p>
            </Card>
          ))}
        </div>

        {!isPracticing ? (
          <>
            {/* Technique List */}
            <div className="mb-12">
              <h2 className="font-xiaowei text-2xl mb-6 flex items-center gap-3">
                <span className="w-1 h-6 bg-vermilion"></span>
                技法学习
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {techniques.map((tech) => (
                  <Card key={tech.id} className="overflow-hidden cursor-pointer group">
                    <div className="flex flex-col md:flex-row">
                      <div className="md:w-1/3 h-48 md:h-auto relative overflow-hidden">
                        <img
                          src={tech.image}
                          alt={tech.name}
                          className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                        />
                        <div className="absolute top-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded-sm">
                          {tech.difficulty}
                        </div>
                      </div>
                      <div className="p-5 md:w-2/3">
                        <h3 className="font-xiaowei text-xl mb-2 group-hover:text-vermilion transition-colors">
                          {tech.name}
                        </h3>
                        <p className="text-charcoal/70 text-sm mb-4">{tech.description}</p>
                        <div className="space-y-2 mb-4">
                          {tech.steps.slice(0, 2).map((step, idx) => (
                            <div key={idx} className="flex items-start gap-2 text-xs text-charcoal/60">
                              <span className="w-4 h-4 bg-ink-black/5 rounded-full flex items-center justify-center flex-shrink-0 text-[10px]">
                                {idx + 1}
                              </span>
                              <span>{step}</span>
                            </div>
                          ))}
                        </div>
                        <Button onClick={() => handlePractice(tech)} variant="outline" className="text-sm px-4 py-2">
                          开始练习
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            {/* Reference Info */}
            <div className="bg-white rounded-sm border border-ink-black/5 p-8">
              <h2 className="font-xiaowei text-2xl mb-6">皮影戏小知识</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="font-bold text-ink-black mb-2">操纵工具</h4>
                  <ul className="text-sm text-charcoal/70 space-y-1">
                    <li>• 主签（颈签）- 控制身体</li>
                    <li>• 手签（左右签）- 控制手臂</li>
                    <li>• 影窗 - 白色半透明幕布</li>
                    <li>• 灯光 - 投射光源</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-bold text-ink-black mb-2">常见剧目</h4>
                  <ul className="text-sm text-charcoal/70 space-y-1">
                    <li>• 火焰驹（陕西皮影）</li>
                    <li>• 五峰会（唐山皮影）</li>
                    <li>• 白蛇传（多流派）</li>
                    <li>• 三打白骨精（山东皮影）</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-bold text-ink-black mb-2">代表传承人</h4>
                  <ul className="text-sm text-charcoal/70 space-y-1">
                    <li>• 魏金全（唐山皮影）</li>
                    <li>• 张树山（陕西皮影）</li>
                    <li>• 汪天稳（陕西皮影）</li>
                    <li>• 刘永周（山东皮影）</li>
                  </ul>
                </div>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Practice Mode */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left: Video Feed */}
              <div className="lg:col-span-2">
                <Card className="p-4">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="font-xiaowei text-xl">{currentTechnique?.name} - 练习中</h3>
                    <Button onClick={handleStopPractice} variant="outline" className="text-sm">
                      完成练习
                    </Button>
                  </div>
                  <div className="relative aspect-video bg-ink-black rounded-sm overflow-hidden">
                    <HandTracking />
                    <div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-sm p-4 rounded-sm">
                      <p className="text-white text-sm">
                        <span className="text-vermilion font-bold">提示：</span>
                        {currentTechnique?.steps[0]}
                      </p>
                    </div>
                  </div>
                </Card>
              </div>

              {/* Right: Feedback Panel */}
              <div className="lg:col-span-1">
                <Card className="p-6 h-full">
                  <h3 className="font-xiaowei text-xl mb-4">动作要领</h3>
                  <div className="space-y-3 mb-6">
                    {currentTechnique?.steps.map((step, idx) => (
                      <div key={idx} className="flex items-start gap-3">
                        <span className="w-5 h-5 bg-vermilion text-white rounded-full flex items-center justify-center text-xs flex-shrink-0">
                          {idx + 1}
                        </span>
                        <p className="text-sm text-charcoal/70">{step}</p>
                      </div>
                    ))}
                  </div>

                  {feedback && (
                    <div className="border-t border-ink-black/5 pt-4">
                      <div className="mb-4">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-bold">动作完成度</span>
                          <span className="text-vermilion font-bold">{feedback.correctness}%</span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-vermilion to-cyan-glaze transition-all duration-500"
                            style={{ width: `${feedback.correctness}%` }}
                          ></div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-bold text-sm mb-2">改进建议</h4>
                        <ul className="space-y-2">
                          {feedback.suggestions.map((suggestion, idx) => (
                            <li key={idx} className="text-sm text-charcoal/70 flex items-start gap-2">
                              <span className="text-cyan-glaze">•</span>
                              {suggestion}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </Card>
              </div>
            </div>
          </>
        )}

        {feedback && (
          <div className="mt-8 text-center">
            <Card className="inline-block p-8 bg-gradient-to-br from-white to-rice-paper">
              <div className="text-6xl font-calligraphy text-vermilion mb-2">{score}分</div>
              <p className="text-charcoal/60 mb-6">本次练习得分</p>
              <div className="flex gap-4">
                <Button onClick={() => {
                  setFeedback(null);
                  setIsPracticing(false);
                }}>
                  返回继续练习
                </Button>
                <Button variant="outline" onClick={() => window.location.href = '/knowledge-curator'}>
                  了解更多皮影戏知识
                </Button>
              </div>
            </Card>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-ink-black text-rice-paper py-8 border-t-4 border-vermilion">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="font-serif text-sm">皮影戏 - 国家级非物质文化遗产</p>
          <p className="text-xs text-charcoal/60 mt-2">2011 年入选联合国教科文组织人类非物质文化遗产代表作名录</p>
        </div>
      </footer>
    </div>
  );
};

export default ShadowPuppet;
