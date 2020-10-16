## coverage.vim

A simple remote plugin for neovim to display test coverage highlighting from a clover XML report.

To set the search paths for clover files:
```vim
let g:coverage_paths = '.coverage/cov.xml'  " the default is 'cov.xml'
" Or specify a list of glob patterns
let g:coverage_paths = ['.coverage/**/cov.xml', '.somewhere/**/*.xml']
```

To configure the highlights used for covered lines:
```vim
let g:coverage_color = {'highlight': 'CoveredLine', 'ctermbg': 'darkgreen', 'guibg': 'darkgreen'}
" Or use an existing highlight group
let g:coverage_color = {'highlight': 'Keyword'}
```
