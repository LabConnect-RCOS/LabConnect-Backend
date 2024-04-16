import React from "react";
import usePageNavigation from "../../shared/hooks/page-navigation-hook";
import PageNavigation from "../../shared/components/Navigation/PageNavigation";
import BrowseItems from "../components/BrowseItems";

/**import { useEffect, useState } from 'react';

const FetchGetRequest = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDataForPosts = async () => {
      const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts?_limit=8`
      );
      if (!response.ok) {
        setData(null);
        return <div></div>
      }
      let postsData = await response.json();
      setData(postsData);
      setLoading(false);
    };

    fetchDataForPosts();
  }, []);

  return <div></div>;

};*/

const DUMMY_DATA = {
  to: "/staff",
  items: [
    {
      id: "d1",
      title: "Computer Science",
      image:
        "https://www.stevens.edu/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fmviowpldu823%2F3DjsfDKUSWQBfdWMEbecCQ%2F24f09c374ddb299ee332352fd69e4042%2FSES-Computer-Science-1900862161.jpg%3Fw%3D1200%26h%3D675%26q%3D80%26fit%3Dfill&w=2400&q=80",
    },
    {
      id: "d2",
      title: "Physics",
      image:
        "https://www.stevens.edu/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fmviowpldu823%2F3DjsfDKUSWQBfdWMEbecCQ%2F24f09c374ddb299ee332352fd69e4042%2FSES-Computer-Science-1900862161.jpg%3Fw%3D1200%26h%3D675%26q%3D80%26fit%3Dfill&w=2400&q=80",
    },
    {
      id: "d3",
      title: "Biology",
      image:
        "https://www.stevens.edu/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fmviowpldu823%2F3DjsfDKUSWQBfdWMEbecCQ%2F24f09c374ddb299ee332352fd69e4042%2FSES-Computer-Science-1900862161.jpg%3Fw%3D1200%26h%3D675%26q%3D80%26fit%3Dfill&w=2400&q=80",
    },
    {
      id: "d4",
      title: "Engineering",
      image:
        "https://www.stevens.edu/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fmviowpldu823%2F3DjsfDKUSWQBfdWMEbecCQ%2F24f09c374ddb299ee332352fd69e4042%2FSES-Computer-Science-1900862161.jpg%3Fw%3D1200%26h%3D675%26q%3D80%26fit%3Dfill&w=2400&q=80",
    },
  ],
};

const Browse = () => {
  var [pages, switchPage] = usePageNavigation(
    ["Research Centers", "Departments"],
    "Research Centers"
  );
  
  return (
    <section className="flex2 gap-3">
      <PageNavigation
        title="Browse Staff"
        pages={pages}
        switchPage={switchPage}
      />


      {pages.activePage === "Research Centers" && (
        <BrowseItems to={DUMMY_DATA.to} items={DUMMY_DATA.items} />
      )}

      {pages.activePage === "Departments" && (
        <BrowseItems to={DUMMY_DATA.to} items={DUMMY_DATA.items} />
      )}
      <br/><br/>
    </section>
  );
};

export default Browse;
