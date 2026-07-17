import { createContext, useContext, useMemo, useState } from "react";

import { login as apiLogin, setAuthToken } from "./api.js";
import { clearToken, loadToken, saveToken } from "./sessionStorage.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => loadToken());
  setAuthToken(token);

  const value = useMemo(() => ({
    token,
    async login(email, password) {
      const result = await apiLogin(email, password);
      saveToken(result.access_token);
      setAuthToken(result.access_token);
      setToken(result.access_token);
    },
    logout() {
      clearToken();
      setAuthToken(null);
      setToken(null);
    }
  }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
