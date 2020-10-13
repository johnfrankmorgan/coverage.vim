## coverage.vim

A simple remote plugin for neovim to display test coverage highlighting from a clover XML report.

To set the search paths for clover files:
```vim
let g:coverage_paths = '.coverage/cov.xml'  " the default is 'cov.xml'
" or
let g:coverage_paths = ['**/cov.xml']
```

To set the highlight used when displaying coverage:
```vim
" the default is
highlight CoveredLine ctermbg=darkgreen guibg=darkgreen
```
