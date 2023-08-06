/*
Copyright 2020 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in
accordance with the terms of the Adobe license agreement accompanying
it.
*/
export type ImgWithSize = {
  width: number
  height: number
  src: string
}

export interface InputImage {
  src: string
  width: number
  height: number
  [k: string]: any
}

export function instanceOfInputImage(obj: any): obj is InputImage {
  return "src" in obj && "width" in obj && "height" in obj
}

export type ReactGridGalleryImg = {
  thumbnail: string
  src: string
  thumbnailWidth: number
  thumbnailHeight: number
  caption?: string
}
