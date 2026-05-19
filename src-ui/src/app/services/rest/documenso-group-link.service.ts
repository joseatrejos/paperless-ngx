import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { DocumensoGroupLink } from 'src/app/data/documenso-group-link'
import { Results } from 'src/app/data/results'
import { AbstractPaperlessService } from './abstract-paperless-service'

@Injectable({
  providedIn: 'root',
})
export class DocumensoGroupLinkService extends AbstractPaperlessService<DocumensoGroupLink> {
  constructor() {
    super()
    this.resourceName = 'documenso_group_links'
  }

  getByGroup(groupId: number): Observable<Results<DocumensoGroupLink>> {
    return this.list(1, 1, null, null, { group: groupId })
  }

  getMyTeams(): Observable<DocumensoGroupLink[]> {
    return this.http.get<DocumensoGroupLink[]>(this.getResourceUrl(null, 'my-teams'))
  }

  triggerSync(id: number): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(this.getResourceUrl(id, 'sync'), {})
  }
}
