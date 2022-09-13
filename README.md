# MkDocs Version Annotations

This is a simple [MkDocs](https://www.mkdocs.org/) plugin that adds a few simple macros to make it quicker and easier to add self-consistent annotations to your documentation about differences between project versions.

This plugin was originally developed for use with the [Nautobot](https://docs.nautobot.com/) project's documentation but should be reusable.

## Usage

Install this plugin with `pip install mkdocs_version_annotations` and enable it as a plugin in your `mkdocs.yml`. You also should enable the [`admonition`](https://python-markdown.github.io/extensions/admonition/) Markdown extension:

```yaml
markdown_extensions:
  - "admonition"

plugins:
  - "search"
  - "mkdocs-version-annotations"
```

In your documentation, you can then use any of the following macros at the start of any line:

- `+++ 1.0.0` as an annotation that something was added in version 1.0.0 of your project
- `+/- 1.0.0` as a annotation that something was changed in version 1.0.0 of your project
- `--- 1.0.0` as a annotation that something was removed in version 1.0.0 of your project

Because these macros will be transformed into Markdown ["admonitions"](https://python-markdown.github.io/extensions/admonition/), you can optionally include details of the change as text on the following line(s) with a four-space indent, such as:

```markdown
+++ 1.0.0
    Added the following parameters:

    - "mass"
    - "spin"
    - "flavor"
```

which would render in the MkDocs-generated HTML as:

```html
<div class="admonition version-added">
<p class="admonition-title">Added in version 1.0.0</p>
<p>Added the following parameters:</p>
<ul>...</ul>
</div>
```

## Plugin Configuration

By default, these macros will render as the following admonitions, which are suitable for use with [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/) or similar themes that allow for [custom admonition styling](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#custom-admonitions):

```markdown
!!! version-added "Added in version <version>"
```

```markdown
!!! version-changed "Changed in version <version>"
```

```markdown
!!! version-removed "Removed in version <version>"
```

This can be fully customized via configuration, if desired! The following configuration keys can be specified in `mkdocs.yaml` under the `mkdocs-version-annotations` entry:

| Configuration                | Default Value              |
| ---------------------------- | -------------------------- |
| `version_added_admonition`   | `"version-added"`          |
| `version_added_title`        | `"Added in version \\1"`   |
| `version_changed_admonition` | `"version-changed"`        |
| `version_changed_title`      | `"Changed in version \\1"` |
| `version_removed_admonition` | `"version-removed"`        |
| `version_removed_title`      | `"Removed in version \\1"` |

In the `_title` configs, the `\1` (backslash-escaped in YAML as `"\\1"`) corresponds to the version number specified in any given usage of the macro.

So for example, you could configure:

```yaml
plugins:
  - mkdocs-version-annotations:
      version_added_admonition: "info"
      version_added_title: "New in version \\1"
```

in which case a `+++ 1.2.3` macro would now be rendered as:

```markdown
!!! info "New in version 1.2.3"
```

## Styling with `mkdocs-material`

If using [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/), you might want to add something like the following to the `extra.css` for your project documentation in order to have custom styling for each of these three custom admonition types. (If you don't add this, or use a different theme, they should still render nonetheless, most likely using the same styling as generic "info" admonitions.)

```css
:root {     
    /* Icon for "version-added" admonition: Material Design Icons "plus-box-outline" */
    --md-admonition-icon--version-added: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 19V5H5v14h14m0-16a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-8 4h2v4h4v2h-4v4h-2v-4H7v-2h4V7Z"/></svg>');
    /* Icon for "version-changed" admonition: Material Design Icons "delta" */
    --md-admonition-icon--version-changed: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 7.77 18.39 18H5.61L12 7.77M12 4 2 20h20"/></svg>');
    /* Icon for "version-removed" admonition: Material Design Icons "minus-circle-outline" */
    --md-admonition-icon--version-removed: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 20c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8m0-18A10 10 0 0 0 2 12a10 10 0 0 0 10 10 10 10 0 0 0 10-10A10 10 0 0 0 12 2M7 13h10v-2H7"/></svg>');
}

/* "version-added" admonition in green */
.md-typeset .admonition.version-added,
.md-typeset details.version-added {
    border-color: rgb(0, 200, 83);
}
.md-typeset .version-added > .admonition-title,
.md-typeset .version-added > summary {
    background-color: rgba(0, 200, 83, .1);
}
.md-typeset .version-added > .admonition-title::before,
.md-typeset .version-added > summary::before {
    background-color: rgb(0, 200, 83);
    -webkit-mask-image: var(--md-admonition-icon--version-added);
    mask-image: var(--md-admonition-icon--version-added);
}

/* "version-changed" admonition in orange */
.md-typeset .admonition.version-changed,
.md-typeset details.version-changed {
    border-color: rgb(255, 145, 0);
}
.md-typeset .version-changed > .admonition-title,
.md-typeset .version-changed > summary {
    background-color: rgba(255, 145, 0, .1);
}
.md-typeset .version-changed > .admonition-title::before,
.md-typeset .version-changed > summary::before {
    background-color: rgb(255, 145, 0);
    -webkit-mask-image: var(--md-admonition-icon--version-changed);
    mask-image: var(--md-admonition-icon--version-changed);
}

/* "version-removed" admonition in red */
.md-typeset .admonition.version-removed,
.md-typeset details.version-removed {
    border-color: rgb(255, 82, 82);
}
.md-typeset .version-removed > .admonition-title,
.md-typeset .version-removed > summary {
    background-color: rgba(255, 82, 82, .1);
}
.md-typeset .version-removed > .admonition-title::before,
.md-typeset .version-removed > summary::before {
    background-color: rgb(255, 82, 82);
    -webkit-mask-image: var(--md-admonition-icon--version-removed);
    mask-image: var(--md-admonition-icon--version-removed);
}
```

## Development

The development environment for this plugin is based on [`invoke`](http://www.pyinvoke.org/) and [`Poetry`](https://python-poetry.org/). After installing Poetry itself, you can run `poetry shell` followed by `poetry install` to set up a Python virtual environment populated with this plugin's development tool dependencies. You can then use the installed `invoke` command to execute various development tasks:

```
$ invoke --list
Available tasks:

  bandit       Run bandit to validate basic static code security analysis.
  black        Run black to check that Python files are consistently formatted.
  flake8       Run flake8 code analysis.
  pydocstyle   Run pydocstyle to validate docstring formatting adheres to standards.
  pylint       Run pylint code static analysis.
  tests        Run all linters and tests for this repository.
```

After making any code change, it is recommended to run `invoke tests` before committing your code.
