import React, {useState} from "react";
import {Image} from "../types";
import classNames from "classnames";

interface Props {
  images: Image[],
  onSelectionChange: (id: number) => void;
}

export default function PhotosGrid({images, onSelectionChange}: Props) {
  let [selected, setSelected] = useState<number>();

  return (
    <ul
      role="list"
      className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 md:grid-cols-4 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8"
    >
      {images.map((file) => (
        <li key={file.id} className="relative" onClick={() => {
          setSelected(file.id);
          onSelectionChange(file.id);
        }}>
          <div
            className={classNames(
              selected === file.id
                ? 'ring-2 ring-offset-2 ring-indigo-500'
                : 'focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-offset-gray-100 focus-within:ring-indigo-500',
              'group block w-full aspect-w-10 aspect-h-7 rounded-lg bg-gray-100 overflow-hidden'
            )}
          >
            <img
              src={file.image}
              alt=""
              className={classNames(
                selected === file.id ? '' : 'group-hover:opacity-75',
                'object-cover pointer-events-none'
              )}
            />
            <button type="button" className="absolute inset-0 focus:outline-none">
              <span className="sr-only">View details for {file.name}</span>
            </button>
          </div>
          <p className="mt-2 block text-sm font-medium text-gray-900 truncate pointer-events-none">
            {file.name}
          </p>
        </li>
      ))}
    </ul>
  )
}