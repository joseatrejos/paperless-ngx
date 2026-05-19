import { AsyncPipe } from '@angular/common'
import {
  AfterViewInit,
  Component,
  EventEmitter,
  Input,
  Output,
  ViewChild,
  inject,
} from '@angular/core'
import { Router, RouterModule } from '@angular/router'
import {
  NgbModal,
  NgbProgressbarModule,
  NgbTooltipModule,
} from '@ng-bootstrap/ng-bootstrap'
import { NgxBootstrapIconsModule } from 'ngx-bootstrap-icons'
import { of } from 'rxjs'
import { delay, first } from 'rxjs/operators'
import {
  DEFAULT_DISPLAY_FIELDS,
  DisplayField,
  Document,
} from 'src/app/data/document'
import { SETTINGS_KEYS } from 'src/app/data/ui-settings'
import { IfPermissionsDirective } from 'src/app/directives/if-permissions.directive'
import { CorrespondentNamePipe } from 'src/app/pipes/correspondent-name.pipe'
import { CustomDatePipe } from 'src/app/pipes/custom-date.pipe'
import { DocumentTitlePipe } from 'src/app/pipes/document-title.pipe'
import { DocumentTypeNamePipe } from 'src/app/pipes/document-type-name.pipe'
import { IsNumberPipe } from 'src/app/pipes/is-number.pipe'
import { StoragePathNamePipe } from 'src/app/pipes/storage-path-name.pipe'
import { UsernamePipe } from 'src/app/pipes/username.pipe'
import { DocumentService } from 'src/app/services/rest/document.service'
import { DocumensoGroupLinkService } from 'src/app/services/rest/documenso-group-link.service'
import { ConfigService } from 'src/app/services/config.service'
import { SettingsService } from 'src/app/services/settings.service'
import { ToastService } from 'src/app/services/toast.service'
import { CustomFieldDisplayComponent } from '../../common/custom-field-display/custom-field-display.component'
import { PreviewPopupComponent } from '../../common/preview-popup/preview-popup.component'
import { TagComponent } from '../../common/tag/tag.component'
import { DocumensoTeamSelectorComponent } from '../../common/documenso-team-selector/documenso-team-selector.component'
import { LoadingComponentWithPermissions } from '../../loading-component/loading.component'

@Component({
  selector: 'pngx-document-card-small',
  templateUrl: './document-card-small.component.html',
  styleUrls: ['./document-card-small.component.scss'],
  imports: [
    DocumentTitlePipe,
    IsNumberPipe,
    PreviewPopupComponent,
    TagComponent,
    CustomFieldDisplayComponent,
    AsyncPipe,
    UsernamePipe,
    CorrespondentNamePipe,
    DocumentTypeNamePipe,
    StoragePathNamePipe,
    IfPermissionsDirective,
    CustomDatePipe,
    RouterModule,
    NgbTooltipModule,
    NgbProgressbarModule,
    NgxBootstrapIconsModule,
  ],
})
export class DocumentCardSmallComponent
  extends LoadingComponentWithPermissions
  implements AfterViewInit
{
  private documentService = inject(DocumentService)
  settingsService = inject(SettingsService)
  private toastService = inject(ToastService)
  private router = inject(Router)
  private configService = inject(ConfigService)
  private modalService = inject(NgbModal)
  private documensoGroupLinkService = inject(DocumensoGroupLinkService)

  DisplayField = DisplayField

  @Input()
  selected = false

  @Output()
  toggleSelected = new EventEmitter()

  @Input()
  document: Document

  @Input()
  displayFields: string[] = DEFAULT_DISPLAY_FIELDS.map((f) => f.id)

  @Output()
  dblClickDocument = new EventEmitter()

  @Output()
  clickTag = new EventEmitter<number>()

  @Output()
  clickCorrespondent = new EventEmitter<number>()

  @Output()
  clickDocumentType = new EventEmitter<number>()

  @Output()
  clickStoragePath = new EventEmitter<number>()

  moreTags: number = null
  isSendingToDocumenso = false

  @ViewChild('popupPreview') popupPreview: PreviewPopupComponent

  ngAfterViewInit(): void {
    of(true)
      .pipe(delay(50))
      .subscribe(() => {
        this.show = true
      })
  }

  getIsThumbInverted() {
    return this.settingsService.get(SETTINGS_KEYS.DARK_MODE_THUMB_INVERTED)
  }

  getThumbUrl() {
    return this.documentService.getThumbUrl(this.document.id)
  }

  getDownloadUrl() {
    return this.documentService.getDownloadUrl(this.document.id)
  }

  get tagIDs() {
    const limit = this.document.notes.length > 0 ? 6 : 7
    if (this.document.tags.length > limit) {
      this.moreTags = this.document.tags.length - (limit - 1)
      return this.document.tags.slice(0, limit - 1)
    } else {
      this.moreTags = null
      return this.document.tags
    }
  }

  mouseLeaveCard() {
    this.popupPreview?.close()
  }

  get notesEnabled(): boolean {
    return this.settingsService.get(SETTINGS_KEYS.NOTES_ENABLED)
  }

  sendToDocumenso(event: Event) {
    event.stopPropagation()
    if (!this.settingsService.get(SETTINGS_KEYS.DOCUMENSO_ENABLED)) {
      this.toastService.show({
        content: $localize`:@@documenso.notConfigured:Documenso is not configured. Set PAPERLESS_DOCUMENSO_URL in docker-compose.env.`,
        classname: 'error',
        delay: 10000,
        action: () => this.router.navigate(['/config']),
        actionName: $localize`Go to configuration`,
      })
      return
    }
    this.configService.getConfig().pipe(first()).subscribe((config) => {
      if (!config.documenso_team_slug) {
        this.toastService.show({
          content: $localize`Documenso Team Slug is not configured. Set it in the configuration page.`,
          classname: 'error',
          delay: 10000,
          action: () => this.router.navigate(['/config']),
          actionName: $localize`Go to configuration`,
        })
        return
      }
      this.documensoGroupLinkService.getMyTeams().pipe(first()).subscribe({
        next: (teams) => {
          if (teams.length === 0) {
            this.toastService.show({
              content: $localize`:@@documenso.noGroup:You do not belong to a group with Documenso configured. Contact an administrator.`,
              classname: 'error',
              delay: 10000,
            })
            return
          }
          const doSend = (groupId: number) => {
            this.isSendingToDocumenso = true
            this.toastService.showInfo($localize`Redirecting to Documenso...`)
            this.documentService
              .sendToDocumenso([this.document.id], groupId)
              .pipe(first())
              .subscribe({
                next: (res) => {
                  this.isSendingToDocumenso = false
                  window.open(res.url, '_blank')
                },
                error: (err) => {
                  this.isSendingToDocumenso = false
                  if (err.status === 403) {
                    this.toastService.show({
                      content: $localize`:@@documenso.noGroup:You do not belong to a group with Documenso configured. Contact an administrator.`,
                      classname: 'error',
                      delay: 10000,
                    })
                  } else {
                    this.toastService.showError(
                      $localize`Error sending document to Documenso`,
                      err
                    )
                  }
                },
              })
          }
          if (teams.length === 1) {
            doSend(teams[0].id)
          } else {
            const modal = this.modalService.open(DocumensoTeamSelectorComponent, { backdrop: 'static' })
            modal.componentInstance.teams = teams
            modal.result.then((groupId: number) => doSend(groupId), () => {})
          }
        },
        error: (err) => {
          this.toastService.showError($localize`Error checking Documenso teams`, err)
        },
      })
    })
  }
}
