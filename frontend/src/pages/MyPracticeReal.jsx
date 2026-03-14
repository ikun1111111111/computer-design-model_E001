import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Button from '../components/Button';
import Card from '../components/Card';
import AbilityRadarChart from '../components/AbilityRadarChart';
import SuEmbroidery from '../assets/Suzhou-embroidery.png';
import PurpleClay from '../assets/Purple-Clay.png';

const API_BASE_URL = 'http://localhost:8002/api/v1';

const MyPractice = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [userProfile, setUserProfile] = useState(null);
  const [practiceRecords, setPracticeRecords] = useState([]);
  const [userWorks, setUserWorks] = useState([]);

  // 用户等级配置
  const levelConfig = {
    beginner: { name: '初学者', color: 'text-charcoal' },
    apprentice: { name: '学徒', color: 'text-cyan-glaze' },
    advanced: { name: '进阶', color: 'text-tea-green' },
    master: { name: '大师', color: 'text-vermilion' },
    grandmaster: { name: '宗师', color: 'text-ink-black' }
  };

  useEffect(() => {
    fetchUserProfile();
    fetchPracticeRecords();
    fetchUserWorks();
  }, []);

  // 获取用户档案
  const fetchUserProfile = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/profile?user_id=1`);
      if (response.ok) {
        const data = await response.json();
        setUserProfile(data);
      }
    } catch (error) {
      console.error('获取用户档案失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 获取练习记录
  const fetchPracticeRecords = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/profile/1/practice-records?limit=5`);
      if (response.ok) {
        const data = await response.json();
        setPracticeRecords(data);
      }
    } catch (error) {
      console.error('获取练习记录失败:', error);
    }
  };

  // 获取用户作品
  const fetchUserWorks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/user/profile/1/works?limit=6`);
      if (response.ok) {
        const data = await response.json();
        setUserWorks(data);
      }
    } catch (error) {
      console.error('获取用户作品失败:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-rice-paper flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-vermilion mx-auto mb-4"></div>
          <p className="text-charcoal font-serif">正在加载修习档案...</p>
        </div>
      </div>
    );
  }

  const levelInfo = levelConfig[userProfile?.user?.level] || levelConfig.beginner;

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
            <div className={`text-6xl font-serif ${levelInfo.color}`}>
              {userProfile?.user?.level === 'grandmaster' ? 'Lv.5' :
               userProfile?.user?.level === 'master' ? 'Lv.4' :
               userProfile?.user?.level === 'advanced' ? 'Lv.3' :
               userProfile?.user?.level === 'apprentice' ? 'Lv.2' : 'Lv.1'}
            </div>
            <div className="text-sm text-charcoal/60 font-sans tracking-widest uppercase">
              {userProfile?.user?.title || '初学者'}
            </div>
          </div>
        </div>

        {/* 主内容区：左档案 右雷达 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
          {/* 左侧：统计卡片 */}
          <div className="lg:col-span-2">
            <h2 className="font-xiaowei text-2xl mb-6 flex items-center gap-3">
              <span className="w-1 h-6 bg-vermilion"></span>
              修习统计
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <Card className="p-6 text-center">
                <div className="text-4xl font-serif text-ink-black mb-2">
                  {userProfile?.stats?.total_practice_hours || 0}h
                </div>
                <div className="text-xs text-charcoal/60 uppercase tracking-widest">总修习时长</div>
              </Card>

              <Card className="p-6 text-center">
                <div className="text-4xl font-serif text-vermilion mb-2">
                  {userProfile?.stats?.average_accuracy || 0}%
                </div>
                <div className="text-xs text-charcoal/60 uppercase tracking-widest">平均准确率</div>
              </Card>

              <Card className="p-6 text-center">
                <div className="text-4xl font-serif text-cyan-glaze mb-2">
                  {userProfile?.stats?.mastered_crafts || 0}
                </div>
                <div className="text-xs text-charcoal/60 uppercase tracking-widest">掌握技法</div>
              </Card>

              <Card className="p-6 text-center">
                <div className="text-4xl font-serif text-tea-green mb-2">
                  {userProfile?.stats?.total_works || 0}
                </div>
                <div className="text-xs text-charcoal/60 uppercase tracking-widest">完成作品</div>
              </Card>
            </div>

            {/* 最近练习记录 */}
            <h3 className="font-xiaowei text-xl mt-10 mb-4">最近练习</h3>
            <div className="space-y-4">
              {practiceRecords.length > 0 ? (
                practiceRecords.map((record) => (
                  <Card key={record.id} className="p-4 flex flex-col md:flex-row gap-4 items-center">
                    <div className="w-16 h-16 bg-gray-100 rounded-sm overflow-hidden flex-shrink-0">
                      <img
                        src={record.craft_id?.includes('embroidery') ? SuEmbroidery : PurpleClay}
                        alt={record.craft_name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="flex-grow">
                      <h4 className="font-xiaowei text-lg">{record.craft_name}</h4>
                      <p className="text-xs text-charcoal/60">
                        {new Date(record.completed_at).toLocaleDateString('zh-CN')}
                      </p>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-serif text-vermilion">{record.score.toFixed(0)}分</div>
                      <div className="text-xs text-charcoal/60">准确率 {record.accuracy.toFixed(0)}%</div>
                    </div>
                  </Card>
                ))
              ) : (
                <Card className="p-8 text-center text-charcoal/60">
                  暂无练习记录，快去开始修习吧！
                </Card>
              )}
            </div>
          </div>

          {/* 右侧：能力雷达图 */}
          <div>
            <h2 className="font-xiaowei text-2xl mb-6 flex items-center gap-3">
              <span className="w-1 h-6 bg-cyan-glaze"></span>
              能力五维
            </h2>
            <Card className="p-6">
              {userProfile?.abilities ? (
                <AbilityRadarChart
                  abilities={userProfile.abilities}
                  width={280}
                  height={280}
                />
              ) : (
                <div className="h-64 flex items-center justify-center text-charcoal/60">
                  暂无能力数据
                </div>
              )}

              {/* 等级进度条 */}
              <div className="mt-6 pt-6 border-t border-ink-black/5">
                <div className="flex justify-between text-sm mb-2">
                  <span className="font-bold">当前等级</span>
                  <span className={levelInfo.color}>{userProfile?.user?.title}</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-vermilion to-cyan-glaze"
                    style={{ width: `${(userProfile?.user?.experience_points % 1000) / 10}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-charcoal/60 mt-1">
                  <span>EXP: {userProfile?.user?.experience_points}</span>
                  <span>下一级：1000</span>
                </div>
              </div>
            </Card>

            {/* 快捷操作 */}
            <div className="mt-6 space-y-3">
              <Button
                className="w-full"
                onClick={() => navigate('/vision-mentor?scenario=embroidery')}
              >
                继续练习苏绣
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => navigate('/craft-library')}
              >
                浏览技艺库
              </Button>
            </div>
          </div>
        </div>

        {/* 作品集 */}
        <h2 className="font-xiaowei text-2xl mb-6 flex items-center gap-3">
          <span className="w-1 h-6 bg-tea-green"></span>
          我的作品
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {userWorks.length > 0 ? (
            userWorks.map((work) => (
              <Card key={work.id} className="overflow-hidden group cursor-pointer">
                <div className="aspect-[4/3] overflow-hidden bg-gray-100">
                  <img
                    src={work.image_url}
                    alt={work.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-xiaowei text-lg mb-1">{work.title}</h3>
                  <p className="text-xs text-charcoal/60 mb-2">{work.craft_name}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-cyan-glaze bg-cyan-glaze/10 px-2 py-1 rounded-sm">
                      {work.ai_generated ? 'AI 生成' : '手作'}
                    </span>
                    <span className="text-xs text-charcoal/40">
                      {new Date(work.created_at).toLocaleDateString('zh-CN')}
                    </span>
                  </div>
                </div>
              </Card>
            ))
          ) : (
            <Card className="md:col-span-3 p-8 text-center text-charcoal/60">
              暂无作品，完成练习后你的作品会出现在这里
            </Card>
          )}
        </div>

        {/* 证书区域 */}
        <h2 className="font-xiaowei text-2xl mt-12 mb-6 flex items-center gap-3">
          <span className="w-1 h-6 border-vermilion"></span>
          我的证书
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-4 border-double border-ink-black/10 p-8 bg-rice-paper text-center relative overflow-hidden group hover:border-vermilion/30 transition-colors cursor-pointer">
            <div className="absolute top-0 right-0 w-16 h-16 bg-vermilion/10 rounded-bl-full"></div>
            <div className="font-calligraphy text-4xl mb-4 text-ink-black">结业证书</div>
            <p className="text-sm text-charcoal/60 mb-6 font-serif">
              兹证明 李明 完成<br />苏绣初级课程修习
            </p>
            <div className="text-xs text-charcoal/40 font-sans tracking-widest">2026.02.15</div>
            <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity text-vermilion text-sm font-bold">
              点击下载
            </div>
          </Card>
        </div>

      </main>

      {/* Footer */}
      <footer className="bg-ink-black text-rice-paper py-8 border-t-4 border-vermilion">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="font-serif text-sm">数字传承人 · 修习档案</p>
          <p className="text-xs text-charcoal/60 mt-2">记录每一次成长的足迹</p>
        </div>
      </footer>
    </div>
  );
};

export default MyPractice;
