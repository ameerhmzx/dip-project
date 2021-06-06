import {PencilIcon} from "@heroicons/react/solid";
import React, {useEffect, useState} from "react";
import {Image} from "../types";
import {sortMeta} from "../meta";

interface Props {
  currentFile?: Image,
}

function FacesLayer({currentFile}: Required<Props>) {
  // 319 is max image size when rendered;
  let scaledPxUnit = currentFile.width / 319;

  return (
    <svg className="w-full absolute inset-0 z-10 faces"
         viewBox={`0 0 ${currentFile.width} ${currentFile.height}`}
         strokeWidth={scaledPxUnit * 4 + 'px'}>
      {
        currentFile.faces.map(({bbox, person}) => {
          let [x, y, width, height] = bbox;

          return (
            <>
              <rect className="face-bbox" x={x} y={y} width={width} height={height} rx={scaledPxUnit * 3 + 'px'}/>
              {
                person
                  ? <>
                    <rect className="text-bg" x={x} y={y + height} width={width} height={16 * scaledPxUnit}/>
                    <text fontSize={scaledPxUnit * 12} x={x + scaledPxUnit * 4} y={y + height + scaledPxUnit * 12}>
                      {person.name}
                    </text>
                  </>
                  : <></>
              }
            </>
          );
        })
      }
    </svg>
  )
}

export default function DetailsPane({currentFile}: Props) {
  if (!currentFile) return <span/>

  return (
    <aside className="hidden w-96 bg-white p-8 border-l border-gray-200 overflow-y-auto lg:block">
      <div className="pb-16 space-y-6">
        <div>
          <div className="block w-full rounded-lg overflow-hidden relative">
            <img src={currentFile.image} alt="" className="w-full"/>
            <FacesLayer currentFile={currentFile}/>
          </div>

          <div className="mt-4">
            <h2 className="text-lg font-medium text-gray-900">
              <span className="sr-only">Details for </span>
              {currentFile.name}
            </h2>
            <div className="mt-2 flex items-center justify-between">
              {
                currentFile.description
                  ? <p className="text-sm text-gray-600">{currentFile.description}</p>
                  : <p className="text-sm text-gray-500 italic">Add a description to this image.</p>
              }
              <button
                type="button"
                className="bg-white rounded-full h-8 w-8 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <PencilIcon className="h-5 w-5" aria-hidden="true"/>
                <span className="sr-only">Add description</span>
              </button>
            </div>
          </div>
        </div>
        {
          currentFile.meta
            ? <div>
              <h3 className="font-medium text-gray-900">Information</h3>
              <dl className="mt-2 border-t border-b border-gray-200 divide-y divide-gray-200">
                {Object.entries(sortMeta(currentFile.meta)).map(([key, val]) => (
                  <div key={key} className="py-3 flex justify-between text-sm font-medium">
                    {
                      <>
                        <dt className="text-gray-500 mr-4">{key}</dt>
                        <dd className="text-gray-900 truncate" title={val as string}>{val as string}</dd>
                      </>
                    }
                  </div>
                ))}
              </dl>
            </div>
            : <></>
        }
        <div className="flex">
          <button
            type="button"
            className="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Download
          </button>
          <button
            type="button"
            className="flex-1 ml-3 bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Delete
          </button>
        </div>
      </div>
    </aside>
  )
}