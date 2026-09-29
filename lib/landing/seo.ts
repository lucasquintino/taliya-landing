export const TALIYA_SITE_ORIGIN = "https://www.taliya.com.br";

export function absoluteSiteUrl(path: string) {
  return new URL(path, TALIYA_SITE_ORIGIN).toString();
}
