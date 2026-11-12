/**
 * The video id from any common YouTube link — watch, youtu.be, shorts, embed —
 * or null. Shared by the Studio's validation and the post renderer, so a link
 * the Studio accepts is one the site can embed.
 */
export function youtubeId(url: string): string | null {
  const match = url.match(
    /(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([\w-]{11})/,
  );
  return match ? match[1] : null;
}
