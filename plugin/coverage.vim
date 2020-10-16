if !exists('g:coverage_paths')
  let g:coverage_paths = 'cov.xml'
endif

if !exists('g:coverage_color')
  let g:coverage_color = {'highlight': 'CoveredLine', 'ctermbg': 'darkgreen', 'guibg': 'darkgreen'}
endif
