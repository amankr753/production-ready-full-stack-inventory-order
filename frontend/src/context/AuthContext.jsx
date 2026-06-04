import { createContext, useContext, useEffect, useMemo, useState } from "react";

import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("accessToken")));

  useEffect(() => {
    if (!localStorage.getItem("accessToken")) return;
    api
      .get("/auth/profile")
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const { data } = await api.post("/auth/login", { email, password });
    localStorage.setItem("accessToken", data.access_token);
    localStorage.setItem("refreshToken", data.refresh_token);
    const profile = await api.get("/auth/profile");
    setUser(profile.data);
  }

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      async register(payload) {
        await api.post("/auth/register", payload);
        await login(payload.email, payload.password);
      },
      logout() {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        setUser(null);
      }
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
