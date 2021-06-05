import {PencilIcon} from "@heroicons/react/solid";
import React from "react";
import {Image} from "../types";

interface Props {
  currentFile?: Image,
}

export default function DetailsPane({currentFile}: Props) {
  if (!currentFile) return <span />

  return (
    <aside className="hidden w-96 bg-white p-8 border-l border-gray-200 overflow-y-auto lg:block">
      <div className="pb-16 space-y-6">
        <div>
          <div className="block w-full rounded-lg overflow-hidden">
            <img src={currentFile.image} alt="" className="object-cover w-full"/>
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
        <div>
          <h3 className="font-medium text-gray-900">Information</h3>
          <dl className="mt-2 border-t border-b border-gray-200 divide-y divide-gray-200">
            {currentFile.meta !== null && Object.keys(currentFile.meta).map((key) => (
              <div key={key} className="py-3 flex justify-between text-sm font-medium">
                <dt className="text-gray-500 mr-4">{key}</dt>
                <dd className="text-gray-900">{currentFile.meta[key]}</dd>
              </div>
            ))}
          </dl>
        </div>
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