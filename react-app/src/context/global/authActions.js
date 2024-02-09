import useGlobalContext from "./useGlobalContext";
import { useCookies } from "react-cookie";

const useAuthActions = () => {
  const { dispatch } = useGlobalContext();
  const [cookie, setCookie, removeCookie] = useCookies(["userCookie"]);

  async function login(state) {
    // make fake call to server

    async function getDetails() {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({
            loggedIn: true,
            id: "d1",
            name: "John Doe",
            email: "johnd@rpi.edu",
            role: "admin",
            department: "Computer Science",
            researchCenter: "AI",
          });
        }, 500);
      });
    }

    const response = await getDetails();

    // if response, dispatch and set cookies
    setCookie("userCookie", response, {
      path: "/",
    });

    response && dispatch({ type: "login", payload: response });
  }

  const logout = () => {
    removeCookie("userCookie", {
      path: "/",
    });
    dispatch({ type: "logout" });
  };

  return { login, logout };
};

export default useAuthActions;
