import React, {useState} from 'react'

import Sidebar from "./components/sidebar";
import DetailsPane from "./components/details-pane";
import PhotosGrid from "./components/photos-grid";
import Images from './Images';

export default function() {
  let [selectedId, setSelected] = useState<number>();

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

              <section className="mt-8 pb-16">
                <PhotosGrid images={Images} onSelectionChange={(id) => setSelected(id)}/>
              </section>
            </div>
          </main>

          <DetailsPane currentFile={Images.find((i) => i.id === selectedId)}/>
        </div>
      </div>
    </div>
  )
}
