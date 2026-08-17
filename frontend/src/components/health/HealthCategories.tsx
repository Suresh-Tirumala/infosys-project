import React from 'react';
import { useNavigate } from 'react-router-dom';

const categories = [
  { id: 'fever', name: 'Fever', icon: '🌡️', color: 'bg-red-50 text-red-700 border-red-200' },
  { id: 'headache', name: 'Headache', icon: '🤕', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  { id: 'cold-flu', name: 'Cold & Flu', icon: '🤧', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  { id: 'cough', name: 'Cough', icon: '😷', color: 'bg-orange-50 text-orange-700 border-orange-200' },
  { id: 'stomach', name: 'Stomach', icon: '🤢', color: 'bg-yellow-50 text-yellow-700 border-yellow-200' },
  { id: 'skin', name: 'Skin', icon: '🖐️', color: 'bg-pink-50 text-pink-700 border-pink-200' },
  { id: 'allergies', name: 'Allergies', icon: '🌼', color: 'bg-green-50 text-green-700 border-green-200' },
  { id: 'sleep', name: 'Sleep', icon: '😴', color: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
  { id: 'nutrition', name: 'Nutrition', icon: '🍎', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
  { id: 'mental', name: 'Mental Health', icon: '🧠', color: 'bg-cyan-50 text-cyan-700 border-cyan-200' },
  { id: 'womens', name: "Women's Health", icon: '♀️', color: 'bg-rose-50 text-rose-700 border-rose-200' },
  { id: 'mens', name: "Men's Health", icon: '♂️', color: 'bg-sky-50 text-sky-700 border-sky-200' },
  { id: 'children', name: "Children's Health", icon: '👶', color: 'bg-amber-50 text-amber-700 border-amber-200' },
  { id: 'general', name: 'General', icon: '💊', color: 'bg-gray-50 text-gray-700 border-gray-200' },
];

const HealthCategories: React.FC = () => {
  const navigate = useNavigate();

  const handleCategoryClick = (categoryId: string, categoryName: string) => {
    navigate(`/chat?category=${categoryId}&topic=${encodeURIComponent(categoryName)}`);
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
      {categories.map((cat) => (
        <button
          key={cat.id}
          onClick={() => handleCategoryClick(cat.id, cat.name)}
          className={`p-4 rounded-xl border-2 ${cat.color} hover:scale-105
                     transition-all duration-200 text-center group`}
        >
          <span className="text-2xl block mb-2">{cat.icon}</span>
          <span className="text-sm font-medium block">{cat.name}</span>
        </button>
      ))}
    </div>
  );
};

export default HealthCategories;
