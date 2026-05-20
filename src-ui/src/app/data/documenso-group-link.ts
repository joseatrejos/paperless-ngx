import { ObjectWithId } from './object-with-id'

export interface DocumensoGroupLink extends ObjectWithId {
  group?: number
  group_name?: string
  documenso_org_name?: string
  is_configured?: boolean
  has_token?: boolean
}
