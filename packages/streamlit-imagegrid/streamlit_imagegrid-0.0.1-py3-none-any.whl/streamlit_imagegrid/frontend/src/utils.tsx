/*
Copyright 2020 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in
accordance with the terms of the Adobe license agreement accompanying
it.
*/
/**
 *
 * @param src Image Url
 * @param idx Index in input array. Since we allow a mix of urls and objects in our input images array
 * we keep the index in order to restore the order of the images intended by the user.
 */

import { ReactGridGalleryImg } from "./types"

//TODO: move to utils folder
export function getImageSize(
  src: string,
  idx: number
): Promise<[number, ReactGridGalleryImg]> {
  let width: number
  let height: number

  return new Promise<[number, ReactGridGalleryImg]>((resolve, reject) => {
    const newImg = new Image()
    newImg.onload = function () {
      height = newImg.height
      width = newImg.width
      console.log("The image size is " + width + "*" + height)
      resolve([
        idx,
        {
          thumbnailWidth: width,
          thumbnailHeight: height,
          src: src,
          thumbnail: src,
        },
      ])
    }

    //if there is an error loading the image.
    newImg.onerror = (e) => {
      console.error(e)
      reject(e)
    }
    newImg.src = src // this must be done AFTER setting onload
  })
}
