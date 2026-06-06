declare module "*.mdx" {
  export const metadata: {
    title: string
    date: string
    description: string
  }
  const component: React.ComponentType
  export default component
}
