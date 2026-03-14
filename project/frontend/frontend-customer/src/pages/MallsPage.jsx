// ============================================================
// src/pages/MallsPage.jsx — หน้าเลือกห้าง
// ============================================================
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMall } from '../context/MallContext';
import { useFetch } from '../hooks/useFetch';
import { mallAPI } from '../services/api';
import BottomNav from '../components/layout/BottomNav';
import Icon from '../components/Icons';
import { T } from '../theme';

const THEMES = [
  { iconBg: '#C7D2FE', color: '#4338CA' },
  { iconBg: '#BBF7D0', color: '#15803D' },
  { iconBg: '#FED7AA', color: '#C2410C' },
  { iconBg: '#E9D5FF', color: '#7E22CE' },
];

function MallCard({ mall, onClick }) {
  const [pressed, setPressed] = useState(false);
  const theme = THEMES[mall.id % THEMES.length];
  return (
    <div
      onClick={onClick}
      onPointerDown={() => setPressed(true)}
      onPointerUp={() => setPressed(false)}
      onPointerLeave={() => setPressed(false)}
      style={{
        display: 'flex', alignItems: 'center', gap: 14,
        background: T.white, borderRadius: 14,
        padding: '14px 16px', marginBottom: 10,
        cursor: 'pointer', border: `1px solid ${T.cardBorder}`,
        boxShadow: pressed ? '0 1px 2px rgba(0,0,0,0.04)' : '0 2px 10px rgba(0,0,0,0.07)',
        transform: pressed ? 'scale(0.98)' : 'scale(1)',
        transition: 'all 0.12s ease',
      }}
    >
      <div style={{ width: 52, height: 52, borderRadius: 12, background: theme.iconBg, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon name="building" size={26} color={theme.color} strokeWidth={1.6} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: 600, fontSize: 15, color: T.textPrimary, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{mall.name}</div>
        <div style={{ color: T.textSecondary, fontSize: 13, marginTop: 3, display: 'flex', alignItems: 'center', gap: 4 }}>
          <Icon name="map-pin" size={12} color={T.textMuted} /> {mall.location}
        </div>
        <div style={{ color: T.textMuted, fontSize: 12, marginTop: 2 }}>{mall.store_count} stores</div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 6, flexShrink: 0 }}>
        {mall.is_popular && (
          <span style={{ fontSize: 11, fontWeight: 600, background: '#FFFBEB', color: '#92400E', border: '1px solid #FDE68A', borderRadius: 20, padding: '2px 8px', display: 'flex', alignItems: 'center', gap: 3 }}>
            <Icon name="star" size={10} color="#92400E" strokeWidth={2} /> Popular
          </span>
        )}
        <Icon name="arrow-right" size={16} color={T.textMuted} />
      </div>
    </div>
  );
}

function Skeleton() {
  return (
    <div style={{ display: 'flex', gap: 14, background: T.white, borderRadius: 14, padding: '14px 16px', marginBottom: 10 }}>
      <div style={{ width: 52, height: 52, borderRadius: 12, background: '#eee' }} />
      <div style={{ flex: 1 }}>
        <div style={{ width: '55%', height: 14, background: '#eee', borderRadius: 6, marginBottom: 8 }} />
        <div style={{ width: '40%', height: 12, background: '#f5f5f5', borderRadius: 6 }} />
      </div>
    </div>
  );
}

export default function MallsPage() {
  const navigate = useNavigate();
  const { setSelectedMall, setSelectedFloor } = useMall();
  const [search, setSearch] = useState('');
  const [focused, setFocused] = useState(false);

  const { data: allMalls, loading } = useFetch(() => mallAPI.getAll(), []);
  const { data: recentMalls }       = useFetch(() => mallAPI.getRecent(), []);

  const filtered = allMalls?.filter(m =>
    m.name.toLowerCase().includes(search.toLowerCase()) ||
    m.location.toLowerCase().includes(search.toLowerCase())
  ) ?? [];
  const popular = filtered.filter(m => m.is_popular);

  const handleSelect = (mall) => {
    setSelectedMall(mall);
    setSelectedFloor(null);
    navigate('/');
  };

  return (
    <div style={{ background: T.pageBg, minHeight: '100vh' }}>

      {/* Header */}
      <div style={{ background: T.header, padding: '48px 16px 18px', color: T.white }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
          <button onClick={() => navigate(-1)} style={{ background: T.headerLight, border: 'none', width: 32, height: 32, borderRadius: 9, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Icon name="arrow-left" size={17} color={T.white} />
          </button>
          <div>
            <div style={{ fontWeight: 700, fontSize: 18 }}>Select Mall</div>
            <div style={{ fontSize: 11, opacity: 0.65, marginTop: 1 }}>Choose a shopping mall to explore</div>
          </div>
        </div>

        {/* Search */}
        <div style={{ position: 'relative', borderRadius: 11, boxShadow: focused ? '0 0 0 3px rgba(255,255,255,0.2)' : 'none', transition: 'box-shadow 0.2s' }}>
          <div style={{ position: 'absolute', left: 11, top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}>
            <Icon name="search" size={15} color="rgba(0,0,0,0.3)" />
          </div>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Search malls by name or location..."
            style={{ width: '100%', padding: '10px 36px 10px 36px', borderRadius: 11, border: 'none', fontSize: 13, background: T.white, boxSizing: 'border-box', outline: 'none', color: '#333', fontFamily: 'inherit' }}
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: '#ddd', border: 'none', width: 20, height: 20, borderRadius: '50%', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            >
              <Icon name="x-circle" size={12} color="#666" />
            </button>
          )}
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: '18px 14px 100px' }}>
        {loading ? [1,2,3].map(i => <Skeleton key={i} />) : (
          <>
            {/* Recent */}
            {!search && recentMalls?.length > 0 && (
              <div style={{ marginBottom: 24 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10, fontWeight: 600, fontSize: 13, color: '#555' }}>
                  <Icon name="clock" size={14} color="#999" /> Recent
                </div>
                {recentMalls.map(m => <MallCard key={m.id} mall={m} onClick={() => handleSelect(m)} />)}
              </div>
            )}

            {/* Popular / Results */}
            {popular.length > 0 ? (
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10, fontWeight: 600, fontSize: 13, color: '#555' }}>
                  <Icon name="trending-up" size={14} color="#999" />
                  {search ? `Results for "${search}"` : 'Popular Malls'}
                </div>
                {popular.map(m => <MallCard key={m.id} mall={m} onClick={() => handleSelect(m)} />)}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '60px 20px' }}>
                <Icon name="search" size={38} color="#ddd" style={{ marginBottom: 12 }} />
                <div style={{ fontWeight: 600, fontSize: 15, color: '#555', marginBottom: 6 }}>ไม่พบ Mall</div>
                <button
                  onClick={() => setSearch('')}
                  style={{ marginTop: 10, padding: '8px 20px', borderRadius: 20, background: T.header, color: T.white, border: 'none', fontSize: 13, cursor: 'pointer', fontFamily: 'inherit' }}
                >
                  ล้างคำค้นหา
                </button>
              </div>
            )}
          </>
        )}
      </div>
      <BottomNav />
    </div>
  );
}