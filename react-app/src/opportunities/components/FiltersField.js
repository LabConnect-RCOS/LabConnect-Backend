import React from "react";
import SmallTextButton from "./SmallTextButton";
import SearchBar from "./SearchBar";
import GroupedComponents from "../../shared/components/UIElements/GroupedComponents";
import HorizontalIconButton from "./HorizontalIconButton";
import { PiSlidersHorizontal } from "react-icons/pi";
import { MdCancel } from "react-icons/md";

const FiltersField = ({ deleteFilter, filters }) => {
  return (
    <div>
      <hr />
      <div className="filters-template">
        <div className="filters-search">
          <SearchBar />

          <GroupedComponents gap={2}>
            {filters.map((filter) => {
              return (
                <HorizontalIconButton
                  onClick={deleteFilter}
                  icon={<MdCancel />}
                  key={filter}
                >
                  {filter}
                </HorizontalIconButton>
              );
            })}
          </GroupedComponents>
        </div>

        <SmallTextButton className="all-filters-btn" special={true}>
          <PiSlidersHorizontal />
          All Filters
        </SmallTextButton>
      </div>
      <hr />
    </div>
  );
};

export default FiltersField;
