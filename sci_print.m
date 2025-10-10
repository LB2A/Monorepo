function sci_print(x, unit)
  if nargin < 2
    unit = '';
  end

  prefixes = {'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T'};
  powers = -12:3:12; % da 10^-12 a 10^12
  idx = find(abs(x) >= 10.^(powers), 1, 'last');
  if isempty(idx)
    idx = 5; % caso 1 (unità base)
  end

  scaled = x / 10^(powers(idx));
  printf('%.3f %s%s (×10^%d %s)\n', scaled, prefixes{idx}, unit, powers(idx), unit);
end
