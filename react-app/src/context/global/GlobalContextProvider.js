import React, { useEffect } from "react";
import { Cookies, useCookies } from "react-cookie";
import globalContext from "./GlobalContext";
import { useReducer } from "react";
import useGlobalContext from "./useGlobalContext";

// log in function

const GlobalContextProvider = ({ children }) => {
  // unpack cookies
  const [cookies, setCookie, removeCookie] = useCookies(["userCookie"]);
  
  const unpackCookies = () => {
    const user = cookies.userCookie || null;

    if (!user) {
      //   if no user cookie, create one
      const userInfo = {
        loggedIn: false,
      };
      setCookie("userCookie", userInfo, {
        path: "/"
      });
      return userInfo;
    } else {
      return user;
    }
  };
  
  function reducer(state, action) {
    switch (action.type) {
      case "login":
        return { ...state, loggedIn: true, ...action.payload };
      case "logout":
        return { loggedIn: false };
      default:
        return state;
    }
  }

  const [state, dispatch] = useReducer(reducer, unpackCookies());
  
  useEffect(() => {
    // login(state);
  }, []);
  
  

  return (
    <globalContext.Provider value={{ ...state, dispatch }}>
      {children}
    </globalContext.Provider>
  );
};

// export provider and dispatch
export { GlobalContextProvider };
