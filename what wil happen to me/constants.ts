
import { Role } from './types';

export const ROLES: Role[] = [
  {
    id: 'physicist',
    name: '张量子',
    title: '物理学家',
    avatar: 'https://picsum.photos/seed/quirky-professor/200/200',
    color: 'bg-blue-400',
    personality: '严谨、INTJ、喜欢用公式和重力数据吐槽，每次回答不超过三句话。'
  },
  {
    id: 'blogger',
    name: '王杠杠',
    title: '吐槽博主',
    avatar: 'https://picsum.photos/seed/cheeky-blogger/200/200',
    color: 'bg-pink-400',
    personality: '毒舌、ENTP、流量至上、玩梗高手、初中学历风格，只需要犀利吐槽。'
  },
  {
    id: 'advisor',
    name: '赵稳妥',
    title: '安全顾问',
    avatar: 'https://picsum.photos/seed/nervous-officer/200/200',
    color: 'bg-orange-400',
    personality: '极度焦虑、ISFJ、有过跳伞创伤、会放大所有安全隐患，只关心生存概率。'
  },
  {
    id: 'writer',
    name: '刘脑洞',
    title: '科幻作家',
    avatar: 'https://picsum.photos/seed/dreamy-artist/200/200',
    color: 'bg-purple-400',
    personality: '脑洞大开、ENFP、天马行空、具有哲学深度，不考虑现实逻辑，只管好玩。'
  }
];

export const PRESET_OPTIONS = {
  jumpHeight: ["高空（10,000米）", "商用高度（9,000米）", "低空（1,000米）", "极低空（200米）"],
  balloonSize: ["巨型（几十平）", "中型（几平）", "小型（1平以内）"],
  heliumRate: ["快速（秒充）", "中速（十几秒）", "慢速（分钟级）"],
  weight: ["50kg", "70kg", "90kg", "110kg"],
  landingScene: ["大海", "城市高楼", "荒野平地", "森林", "雪山"]
};

export const INITIAL_QUESTIONS = [
  "气球要多大才能让我飘起来？",
  "空中充气下降速度会变慢吗？",
  "氦气罐重量会压垮我吗？",
  "从多高跳下来最安全？",
  "气球炸了怎么办？",
  "可以作为直播素材吗？"
];
