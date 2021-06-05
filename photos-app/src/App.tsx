import React from 'react'
import classNames from "classnames";

import Sidebar from "./components/sidebar";
import DetailsPane from "./components/details-pane";

const files = [
  {
    name: 'IMG_4985.HEIC',
    size: '3.9 MB',
    source:
      'https://images.unsplash.com/photo-1582053433976-25c00369fc93?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80',
    current: true,
  },
  // More files...
]
const currentFile = {
  name: 'IMG_4985.HEIC',
  size: '3.9 MB',
  source:
    'https://images.unsplash.com/photo-1582053433976-25c00369fc93?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80',
  information: {
    'Uploaded by': 'Marie Culver',
    Created: 'June 8, 2020',
    'Last modified': 'June 8, 2020',
    Dimensions: '4032 x 3024',
    Resolution: '72 x 72',
  },
  sharedWith: [
    {
      id: 1,
      name: 'Aimee Douglas',
      imageUrl:
        'https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=1024&h=1024&q=80',
    },
    {
      id: 2,
      name: 'Andrea McMillan',
      imageUrl:
        'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixqx=oilqXxSqey&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  ],
}

function App() {
  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Sidebar/>

      <div className="flex-1 flex flex-col overflow-hidden">

        <div className="flex-1 flex items-stretch overflow-hidden">
          <main className="flex-1 overflow-y-auto">
            <div className="pt-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex">
                <h1 className="flex-1 text-2xl font-bold text-gray-900">Photos</h1>
              </div>

              {/* Gallery */}
              <section className="mt-8 pb-16">
                <ul
                  role="list"
                  className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 md:grid-cols-4 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8"
                >
                  {files.map((file) => (
                    <li key={file.name} className="relative">
                      <div
                        className={classNames(
                          file.current
                            ? 'ring-2 ring-offset-2 ring-indigo-500'
                            : 'focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-offset-gray-100 focus-within:ring-indigo-500',
                          'group block w-full aspect-w-10 aspect-h-7 rounded-lg bg-gray-100 overflow-hidden'
                        )}
                      >
                        <img
                          src={file.source}
                          alt=""
                          className={classNames(
                            file.current ? '' : 'group-hover:opacity-75',
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
                      <p className="block text-sm font-medium text-gray-500 pointer-events-none">{file.size}</p>
                    </li>
                  ))}
                </ul>
              </section>
            </div>
          </main>

          <DetailsPane currentFile={currentFile}/>
        </div>
      </div>
    </div>
  )
}

export default App
