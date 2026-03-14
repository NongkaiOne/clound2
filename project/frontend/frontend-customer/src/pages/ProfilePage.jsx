// ============================================================
// src/pages/ProfilePage.jsx — Login / Register / Profile
// ============================================================
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';
import BottomNav from '../components/layout/BottomNav';
import Icon from '../components/Icons';
import { T } from '../theme';

function InputField({ label, type = 'text', value, onChange, placeholder }) {
  const [focused, setFocused] = useState(false);
  return (
    <div style={{ marginBottom: 14 }}>
      <label style={{ display: 'block', fontSize: 13, color: '#555', marginBottom: 5, fontWeight: 500 }}>{label}</label>
      <input
        type={type} value={value} onChange={onChange} placeholder={placeholder}
        onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
        style={{ width: '100%', padding: '11px 13px', borderRadius: 10, border: `1.5px solid ${focused ? T.header : '#e0e0e0'}`, fontSize: 13, outline: 'none', boxSizing: 'border-box', color: '#333', fontFamily: 'inherit', transition: 'border-color 0.15s' }}
      />
    </div>
  );
}

export default function ProfilePage() {
  const navigate = useNavigate();
  const { isLoggedIn, user, login, logout } = useAuth();
  const [mode,     setMode]     = useState('login');
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error,    setError]    = useState('');
  const [loading,  setLoading]  = useState(false);

  const handleLogin = async () => {
    if (!email || !password) { setError('กรุณากรอก Email และ Password'); return; }
    setError(''); setLoading(true);
    try { await login(email, password); navigate('/'); }
    catch (e) { setError(e?.response?.data?.message || 'เข้าสู่ระบบไม่สำเร็จ'); }
    finally { setLoading(false); }
  };

  const handleRegister = async () => {
    if (!username || !email || !password) { setError('กรุณากรอกข้อมูลให้ครบ'); return; }
    setError(''); setLoading(true);
    try { await authAPI.register({ username, email, password }); await login(email, password); navigate('/'); }
    catch (e) { setError(e?.response?.data?.message || 'สมัครสมาชิกไม่สำเร็จ'); }
    finally { setLoading(false); }
  };

  const switchMode = (m) => { setMode(m); setError(''); setEmail(''); setPassword(''); setUsername(''); };

  // ===== หน้า Profile (Login แล้ว) =====
  if (isLoggedIn) {
    return (
      <div style={{ background: T.pageBg, minHeight: '100vh' }}>
        <div style={{ background: T.header, padding: '48px 16px 20px', color: T.white }}>
          <div style={{ fontWeight: 700, fontSize: 17 }}>Profile</div>
          <div style={{ fontSize: 11, opacity: 0.65, marginTop: 1 }}>Smart Mall</div>
        </div>
        <div style={{ padding: '36px 20px 100px', textAlign: 'center' }}>
          <div style={{ width: 82, height: 82, borderRadius: '50%', background: '#e0dce8', border: `3px solid ${T.white}`, boxShadow: '0 4px 16px rgba(0,0,0,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
            <Icon name="user" size={36} color={T.header} strokeWidth={1.4} />
          </div>
          <div style={{ fontWeight: 700, fontSize: 19, color: T.textPrimary, marginBottom: 4 }}>{user?.username || 'User'}</div>
          <div style={{ color: T.textSecondary, fontSize: 14, marginBottom: 32 }}>{user?.email}</div>
          <button
            onClick={logout}
            style={{ background: T.white, color: T.header, border: `1.5px solid ${T.header}`, borderRadius: 11, padding: '11px 40px', fontSize: 14, fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit', display: 'inline-flex', alignItems: 'center', gap: 8 }}
          >
            <Icon name="log-out" size={16} color={T.header} /> ออกจากระบบ
          </button>
        </div>
        <BottomNav />
      </div>
    );
  }

  // ===== หน้า Login / Register =====
  return (
    <div style={{ background: T.pageBg, minHeight: '100vh' }}>
      <div style={{ background: T.header, padding: '48px 16px 20px', color: T.white }}>
        <div style={{ fontWeight: 700, fontSize: 17 }}>Smart Mall</div>
        <div style={{ fontSize: 11, opacity: 0.65, marginTop: 1 }}>Interactive Directory</div>
      </div>

      <div style={{ padding: '18px 16px 100px' }}>

        {/* Login Card */}
        <div style={{ background: T.white, borderRadius: 16, padding: '20px 20px 22px', marginBottom: 14, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
          {/* Avatar */}
          <div style={{ textAlign: 'center', marginBottom: 20 }}>
            <div style={{ width: 70, height: 70, borderRadius: '50%', background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px' }}>
              <Icon name="user" size={32} color={T.header} strokeWidth={1.4} />
            </div>
            <div style={{ fontWeight: 700, fontSize: 17, color: T.textPrimary }}>Welcome to Smart Mall</div>
            <div style={{ color: T.textSecondary, fontSize: 12, marginTop: 5, lineHeight: 1.5 }}>Login or register to save your favorite stores</div>
          </div>

          {/* Mock hint */}
          <div style={{ background: '#f0fff4', border: '1px solid #bbf7d0', borderRadius: 8, padding: '7px 11px', marginBottom: 16, fontSize: 11, color: '#166534' }}>
            🧪 ทดสอบ: <strong>test@mail.com</strong> / <strong>1234</strong>
          </div>

          {mode === 'register' && (
            <InputField label="ชื่อผู้ใช้" value={username} onChange={e => setUsername(e.target.value)} placeholder="ชื่อของคุณ" />
          )}
          <InputField label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="email@example.com" />
          <InputField label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" />

          {error && (
            <div style={{ color: '#b91c1c', fontSize: 12, marginBottom: 12, background: '#fef2f2', border: '1px solid #fecaca', padding: '8px 11px', borderRadius: 8 }}>
              ⚠️ {error}
            </div>
          )}

          {/* ปุ่ม Login / Register */}
          <button
            onClick={mode === 'login' ? handleLogin : handleRegister}
            disabled={loading}
            style={{ width: '100%', padding: '12px', background: loading ? '#888' : T.header, color: T.white, border: 'none', borderRadius: 11, fontSize: 14, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer', marginBottom: 10, fontFamily: 'inherit', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
          >
            <Icon name={mode === 'login' ? 'log-in' : 'user-plus'} size={17} color={T.white} />
            {loading ? 'กำลังดำเนินการ...' : mode === 'login' ? 'Login' : 'Register'}
          </button>

          {/* ปุ่มสลับ mode */}
          <button
            onClick={() => switchMode(mode === 'login' ? 'register' : 'login')}
            style={{ width: '100%', padding: '11px', background: T.white, color: T.header, border: `1.5px solid #ddd`, borderRadius: 11, fontSize: 13, fontWeight: 500, cursor: 'pointer', fontFamily: 'inherit' }}
          >
            {mode === 'login' ? 'สมัครสมาชิก' : '← กลับไปหน้า Login'}
          </button>
        </div>

        {/* Feature Cards */}
        {[
          { icon: 'heart', title: 'Save Favorites', desc: 'Save your favorite stores and products for quick access anytime' },
          { icon: 'building', title: 'Browse Multiple Malls', desc: 'Access directories for multiple shopping malls in your area' },
        ].map(({ icon, title, desc }) => (
          <div key={title} style={{ display: 'flex', alignItems: 'center', gap: 12, background: T.white, borderRadius: 12, padding: '13px 14px', marginBottom: 10, boxShadow: '0 1px 6px rgba(0,0,0,0.06)', border: `1px solid ${T.cardBorder}` }}>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: '#f5f5f5', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Icon name={icon} size={19} color={T.header} strokeWidth={1.6} />
            </div>
            <div>
              <div style={{ fontWeight: 600, fontSize: 13, color: T.textPrimary }}>{title}</div>
              <div style={{ color: T.textSecondary, fontSize: 11, marginTop: 2, lineHeight: 1.4 }}>{desc}</div>
            </div>
          </div>
        ))}
      </div>
      <BottomNav />
    </div>
  );
}