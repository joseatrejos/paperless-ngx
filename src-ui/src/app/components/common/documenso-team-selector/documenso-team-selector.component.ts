import { Component, inject, Input } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import { NgxBootstrapIconsModule } from 'ngx-bootstrap-icons'
import { DocumensoGroupLink } from 'src/app/data/documenso-group-link'

@Component({
  selector: 'pngx-documenso-team-selector',
  templateUrl: './documenso-team-selector.component.html',
  imports: [NgxBootstrapIconsModule],
})
export class DocumensoTeamSelectorComponent {
  activeModal = inject(NgbActiveModal)

  @Input() teams: DocumensoGroupLink[] = []

  selectedId: number | null = null

  confirm() {
    if (this.selectedId !== null) {
      this.activeModal.close(this.selectedId)
    }
  }
}
