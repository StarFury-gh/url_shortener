import { US_API_URL, ACCESS_TOKEN } from "../../constants";

import { useState, useEffect } from "react";

interface UserInfo {
  id: number;
  email: string;
}

interface AuthServerResponse {
  status: boolean;
  id: number;
  email: string;
}

interface AuthState {
  auth: boolean;
  user: UserInfo | null;
}

function useAuth(): AuthState {
  const [authState, setAuthState] = useState<AuthState>({
    auth: false,
    user: null,
  });

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem(ACCESS_TOKEN);

        if (!token) {
          setAuthState({
            auth: false,
            user: null,
          });
          return;
        }

        const response = await fetch(`${US_API_URL}/users/auth`, {
          method: "GET",
          headers: {
            Authorization: token,
          },
        });

        if (!response.ok) {
          throw new Error("Authentication failed");
        }

        const data: AuthServerResponse = await response.json();

        setAuthState({
          auth: true,
          user: { email: data.email, id: data.id },
        });
      } catch (error) {
        console.error("Auth error:", error);
        setAuthState({
          auth: false,
          user: null,
        });
      }
    };

    checkAuth();
  }, []);

  return authState;
}

export default useAuth;
