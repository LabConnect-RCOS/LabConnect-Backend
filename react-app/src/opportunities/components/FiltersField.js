import React, { useState } from "react";
import SmallTextButton from "./SmallTextButton";
import SearchBar from "./SearchBar";
import GroupedComponents from "../../shared/components/UIElements/GroupedComponents";
import HorizontalIconButton from "./HorizontalIconButton";
import { PiSlidersHorizontal } from "react-icons/pi";
import { MdCancel } from "react-icons/md";
import FilterModal from "./FilterModal"; // Import the FilterModal component

const FiltersField = ({ deleteFilter, filters }) => {
  const [showModal, setShowModal] = useState(false);

  // Function to open the modal
  const openModal = () => {
    setShowModal(true);
  };

  // Function to close the modal
  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div>
      <hr />
      <div className="px-3 overflow-x-scroll max-h-20 flex gap-3">
        <div className="flex gap-2 w-full">
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
        {/* Pass openModal function as onClick prop */}
        <SmallTextButton
          className="justify-end w-full"
          special={true}
          onClick={openModal}
        >
          <PiSlidersHorizontal />
          All Filters
        </SmallTextButton>
      </div>
      <hr />
      {/* Render the FilterModal component and pass open/close functions */}
      <FilterModal open={showModal} handleClose={closeModal} />
    </div>
  );
};

export default FiltersField;
