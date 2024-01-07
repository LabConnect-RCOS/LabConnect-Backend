import { useState } from "react";

const usePageNavigation = (views, activeView) => {
    var [pages, setPages] = useState({pages: views, activePage: activeView})
    
    const switchPage = (view) => {
        setPages(()=>{return {...pages, activePage: view}});

    }
    
    return [pages, switchPage];
}

export default usePageNavigation;