import classNames from "classnames";
import React from "react";
import {
  CogIcon,
  CollectionIcon,
  HomeIcon,
  PhotographIcon,
  UserGroupIcon,
  ViewGridIcon as ViewGridIconOutline
} from "@heroicons/react/outline";

const navigation = [
  {name: 'Home', href: '#', icon: HomeIcon, current: false},
  {name: 'All Files', href: '#', icon: ViewGridIconOutline, current: false},
  {name: 'Photos', href: '#', icon: PhotographIcon, current: true},
  {name: 'Shared', href: '#', icon: UserGroupIcon, current: false},
  {name: 'Albums', href: '#', icon: CollectionIcon, current: false},
  {name: 'Settings', href: '#', icon: CogIcon, current: false},
]

export default function Sidebar() {
  return (
    <div className="w-28 bg-indigo-700 overflow-y-auto">
      <div className="w-full py-6 flex flex-col items-center">
        <div className="flex-shrink-0 flex items-center">
          <img
            className="h-8 w-auto"
            src="https://tailwindui.com/img/logos/workflow-mark.svg?color=white"
            alt="Workflow"
          />
        </div>
        <div className="flex-1 mt-6 w-full px-2 space-y-1">
          {navigation.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className={classNames(
                item.current ? 'bg-indigo-800 text-white' : 'text-indigo-100 hover:bg-indigo-800 hover:text-white',
                'group w-full p-3 rounded-md flex flex-col items-center text-xs font-medium'
              )}
              aria-current={item.current ? 'page' : undefined}
            >
              <item.icon
                className={classNames(
                  item.current ? 'text-white' : 'text-indigo-300 group-hover:text-white',
                  'h-6 w-6'
                )}
                aria-hidden="true"
              />
              <span className="mt-2">{item.name}</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}