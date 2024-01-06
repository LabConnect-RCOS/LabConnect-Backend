import React from "react";
import SmallTextButton from "./SmallTextButton";
import SearchBar from "./SearchBar";
import GroupedComponents from "../../shared/components/UIElements/GroupedComponents";
import HorizontalIconButton from "./HorizontalIconButton";
import { PiSlidersHorizontal } from "react-icons/pi";
import { MdCancel } from "react-icons/md";

const FiltersField = () => {
  return (
    <div>
      <hr />
      <div className="px-3 overflow-x-scroll max-h-20 flex gap-3">
        <div className="flex gap-2 w-full">
          <SearchBar />

          <GroupedComponents gap={2}>
            <HorizontalIconButton icon={<MdCancel />}>
              Credit
            </HorizontalIconButton>

            <HorizontalIconButton icon={<MdCancel />}>
              Fall
            </HorizontalIconButton>

            <HorizontalIconButton icon={<MdCancel />}>
              Physics
            </HorizontalIconButton>
          </GroupedComponents>
        </div>

        <SmallTextButton className="justify-end w-full" special={true}>
          <PiSlidersHorizontal />
          All Filters
        </SmallTextButton>
      </div>
      <hr />
    </div>
  );
};

export default FiltersField;
