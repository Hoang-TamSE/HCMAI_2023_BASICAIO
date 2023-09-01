import React, { useState, useRef } from "react";
import { DragDropContainer } from "react-drag-drop-container";

export default function Boxable(props) {
  const { targetKey, label, image, customDragElement, onDelete, bottom } = props;
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const imageRef = useRef(null);

  const handleDragEnd = () => {
    console.log("end");
    const imageRect = imageRef.current.getBoundingClientRect();
    // Get the position of the image after dragging and log it
    console.log({ x: imageRect.left, y: imageRect.top });
    setPosition({
      x: imageRect.left -7,
      y: imageRect.top - parseFloat(bottom.top) - 7,
    });
  };

  const handleDeleteClick = () => {
    console.log("delete");
    onDelete();
  };

  return (
    <div
      style={{
        display: "inline-block",
        position: "absolute",
        top: position.y,
        left: position.x,
      }}
    >
      <DragDropContainer
        targetKey={targetKey}
        dragData={{ label: label }}
        customDragElement={customDragElement}
        onDragEnd={handleDragEnd}
      >
        <div
          style={{
            position: "relative",
            display: "inline-block",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.lastChild.style.display = "block")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.lastChild.style.display = "none")
          }
        >
          <img
            ref={imageRef}
            src={image}
            width="45"
            height="45"
            alt={image}
          />
          <button
            style={{
              position: "absolute",
              top: "-10px",
              right: "-5px",
              backgroundColor: "transparent",
              border: "none",
              color: "red",
              cursor: "pointer",
              fontSize: "1rem",
              display: "none",
            }}
            onClick={handleDeleteClick}
          >
            x
          </button>
        </div>
      </DragDropContainer>
    </div>
  );
}