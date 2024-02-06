import React from "react";
import FiltersField from "../components/FiltersField";
import PostsField from "./PostsField";
import { useReducer } from "react";
import { useCallback } from "react";

const Posts = () => {
  const reducer = (state, action) => {
    switch (action.type) {
      case "REMOVE_FILTER":
        if (action.filter) {
          state.filters = state.filters.filter((item) => item != action.filter);
        }
        return {...state};
      case "ADD_FILTER":
        if (action.filter) {
          state.filters.push(action.filter);
        }
        return {...state};
      case "SET_ACTIVE_ID":
        if (action.id) {
          if (state.jobs.find((job) => job.id === action.id)) {
            state.activeId = action.id;
          }
        }
        return {...state};
      default:
        return state;
    }
  };

  var [jobState, dispatch] = useReducer(reducer, {
    filters: ["Fall", "Credit", "Remote"],
    activeId: "u1",
    jobs: [
      {
        title: "Software Engineer",
        professor: "Turner",
        id: "u1",
        location: "CII",
        season: "Spring",
        year: 2024,
      },
      {
        title: "Physics Research Engineer",
        professor: "Turner",
        id: "u2",
        location: "CII",
        season: "Spring",
        year: 2024,
      },
    ],
  });

  const removeFilter = useCallback((name) => {
    dispatch({ type: "REMOVE_FILTER", filter: name });
  });

  const addFilter = useCallback((name) => {
    dispatch({ type: "ADD_FILTER", filter: name });
  });

  const setActiveId = useCallback((val) => {
    console.log(val);
    dispatch({ type: "SET_ACTIVE_ID", id: val });
  });

  return (
    <section>
      <FiltersField deleteFilter={removeFilter} filters={jobState.filters} />
      <PostsField activeId={jobState.activeId} setActive={setActiveId} />
    </section>
  );
};

export default Posts;
