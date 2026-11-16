function requireLogin(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.redirect('/login');
  }
  next();
}

function requireAdmin(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.redirect('/login');
  }
  if (req.session.user.role !== 'admin') {
    return res.status(403).render('error', {
      user:    req.session.user,
      status:  403,
      message: 'Admin access required.',
    });
  }
  next();
}

module.exports = { requireLogin, requireAdmin };
