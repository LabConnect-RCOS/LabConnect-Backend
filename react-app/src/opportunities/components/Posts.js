import React from "react";
import FiltersField from "../components/FiltersField";
import PostsField from "./PostsField";

const Posts = () => {
  return (
    <section>
      <FiltersField />
      <PostsField />
    </section>
  );
};

export default Posts;
