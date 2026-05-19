import { Component, inject } from '@angular/core'
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms'
import { map, of, switchMap } from 'rxjs'
import {
  EditDialogComponent,
  EditDialogMode,
} from 'src/app/components/common/edit-dialog/edit-dialog.component'
import { DocumensoGroupLink } from 'src/app/data/documenso-group-link'
import { Group } from 'src/app/data/group'
import { DocumensoGroupLinkService } from 'src/app/services/rest/documenso-group-link.service'
import { GroupService } from 'src/app/services/rest/group.service'
import { UserService } from 'src/app/services/rest/user.service'
import { SettingsService } from 'src/app/services/settings.service'
import { ToastService } from 'src/app/services/toast.service'
import { TextComponent } from '../../input/text/text.component'
import { PermissionsSelectComponent } from '../../permissions-select/permissions-select.component'

@Component({
  selector: 'pngx-group-edit-dialog',
  templateUrl: './group-edit-dialog.component.html',
  styleUrls: ['./group-edit-dialog.component.scss'],
  imports: [
    PermissionsSelectComponent,
    TextComponent,
    FormsModule,
    ReactiveFormsModule,
  ],
})
export class GroupEditDialogComponent extends EditDialogComponent<Group> {
  private documensoService = inject(DocumensoGroupLinkService)
  private toastService = inject(ToastService)
  documensoLinkId: number | null = null
  syncingDocumenso = false

  constructor() {
    super()
    this.service = inject(GroupService)
    this.userService = inject(UserService)
    this.settingsService = inject(SettingsService)
  }

  override ngOnInit(): void {
    super.ngOnInit()
    if (this.object?.id) {
      this.documensoService.getByGroup(this.object.id).subscribe({
        next: (results) => {
          if (results.results.length > 0) {
            const link = results.results[0]
            this.documensoLinkId = link.id
            this.objectForm.patchValue({ documenso_org_name: link.documenso_org_name })
          }
        },
        error: (err) => {
          console.error('Error loading Documenso group link', err)
        },
      })
    }
  }

  getCreateTitle() {
    return $localize`Create new user group`
  }

  getEditTitle() {
    return $localize`Edit user group`
  }

  getForm(): FormGroup {
    return new FormGroup({
      name: new FormControl(''),
      permissions: new FormControl([]),
      documenso_org_name: new FormControl(''),
    })
  }

  override save() {
    this.error = null
    const formValues: any = { ...this.objectForm.value }
    const orgName: string = formValues['documenso_org_name'] ?? ''
    delete formValues['documenso_org_name']

    const newObject = Object.assign({}, this.object, formValues) as Group
    const groupResponse =
      this.dialogMode === EditDialogMode.CREATE
        ? this.service.create(newObject)
        : this.service.update(newObject)

    this.networkActive = true

    groupResponse
      .pipe(
        switchMap((savedGroup) => {
          if (!orgName) {
            return of(savedGroup)
          }
          if (this.documensoLinkId) {
            return this.documensoService
              .patch({
                id: this.documensoLinkId,
                documenso_org_name: orgName,
              } as DocumensoGroupLink)
              .pipe(map(() => savedGroup))
          } else {
            return this.documensoService
              .create({
                group: savedGroup.id,
                documenso_org_name: orgName,
              } as DocumensoGroupLink)
              .pipe(map((link) => {
                this.documensoLinkId = link.id
                return savedGroup
              }))
          }
        })
      )
      .subscribe({
        next: (result) => {
          this.activeModal.close()
          this.succeeded.emit(result)
        },
        error: (error) => {
          this.error = error.error
          this.networkActive = false
          this.failed.next(error)
        },
      })
  }

  syncDocumensoUsers() {
    if (!this.documensoLinkId || this.syncingDocumenso) {
      return
    }

    this.syncingDocumenso = true
    this.documensoService.triggerSync(this.documensoLinkId).subscribe({
      next: (res) => {
        this.syncingDocumenso = false
        this.toastService.show({
          content:
            res?.detail ||
            $localize`Documenso sync started for this group.`,
          classname: 'info',
          delay: 7000,
        })
      },
      error: (error) => {
        this.syncingDocumenso = false
        this.toastService.showError(
          $localize`Could not start Documenso sync for this group`,
          error
        )
      },
    })
  }
}
