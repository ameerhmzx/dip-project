import {ImageMeta} from "./types";

let metaCategoryMap = {
  Lens: ['LensMake', 'LensModel'],
  Camera: ['Make', 'Model'],
  Resolution: ['XResolution', 'YResolution']
}

let metaValMap = {
  Lens: (v: Array<string>) => v.join(' '),
  Camera: (v: Array<string>) => v.join(' '),
  Resolution: (v: Array<number>) => v.join('x'),
  GPSInfo: (v: Array<number>) => v.join(', '),
  ApertureValue: (v: number) => v.toFixed(4),
  ShutterSpeedValue: (v: number) => v.toFixed(4),
  ExposureTime: (v: number) => `1/${(1 / v).toFixed()}`,
  DateTime: (v: string) => {
    let date = v.split(' ')
    date = [date[0].replace(/:/g, '-'), date[1]];
    let jsDate = new Date(date.join(' '));

    let formatter = new Intl.DateTimeFormat(
      'en-GB',
      {dateStyle: 'medium', timeStyle: 'short'} as any
    )

    return formatter.format(jsDate)
  },
}

let metaKeyMap = {
  DateTime: 'Creation Time',
  GPSInfo: 'Location',
  ShutterSpeedValue: 'Shutter Speed',
  ISOSpeedRatings: 'ISO Speed Ratings'
}

export function sortMeta(meta: Partial<ImageMeta>) {
  let newMeta = {};

  Object.entries(meta).map(([key, val]) => {
    let newKey = Object.entries(metaCategoryMap).find(([_, v]) => v.includes(key));
    if (newKey) {
      if (newMeta[newKey[0]]) {
        newMeta[newKey[0]].push(val);
      } else {
        newMeta[newKey[0]] = [val];
      }
    } else {
      newMeta[key] = val;
    }
  })

  return Object.fromEntries(
    Object.entries(newMeta)
      .map(([key, val]) => {
        if (metaValMap[key]) {
          val = metaValMap[key](val);
        }

        if (metaKeyMap[key]) {
          key = metaKeyMap[key];
        } else {
          key = key.replace(/([A-Z])/g, ' $1').trim();
        }

        return [key, val];
      })
  );
}