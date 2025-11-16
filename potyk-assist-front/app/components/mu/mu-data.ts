export type Track = {
  title: string
  artist: string
  src: string
  cover: string
}

export type Album = {
  id: string
  title: string
  artist: string
  year: number
  cover: string
  link: string
  track: Track
}

export const featuredAlbums: Album[] = [
  {
    id: 'londinium',
    title: 'Londinium',
    artist: 'Archive',
    year: 1996,
    cover:
      'https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600',
    link: 'https://music.yandex.ru/album/89962',
    track: {
      title: 'So Few Words',
      artist: 'Archive',
      src: '/Archive%20-%20So%20Few%20Words.mp3',
      cover:
        'https://avatars.yandex.net/get-music-content/49876/cbf41616.a.89962-1/600x600',
    },
  },
]


