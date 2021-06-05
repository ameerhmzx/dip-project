import {ImageMeta} from "./types";

let metaMap: {[key: string]: Array<keyof ImageMeta>} = {
  Lens: ['LensMake', 'LensModel'],
  Camera: ['Make', "Model"],

}

export function sortMeta(meta: Partial<ImageMeta>) {

}