export interface ImageMeta {
  ColorProfile: string;
  ColorSpace: string;
  XResolution: number;
  YResolution: number;
  Make: string;
  Model: string;
  Software: string;
  DateTime: string;
  ApertureValue: number;
  ExposureTime: number;
  ShutterSpeedValue: number;
  FocalLength: number;
  ISOSpeedRatings: number;
  MeteringMode: number;
  Flash: number;
  FNumber: number;
  ExposureProgram: number;
  WhiteBalance: number;
  LensMake: string;
  LensModel: string;
  GPSInfo: [number, number];
}

export interface ImageFace {
  id: number;
  bbox: [number, number, number, number];
  confidence: number;
  person: {
    id: number;
    name: string;
  } | null
}

export interface ImageObject {
  id: number;
  bbox: [number, number, number, number];
  confidence: number;
  name: string;
  info: {
    [key: string]: any
  }
}

export interface Image {
  id: number;
  name: string;
  description: string;
  image: string;
  thumbnail: string;
  meta: Partial<ImageMeta>,
  faces: Array<ImageFace>;
  detected_objects: Array<ImageObject>;
}
