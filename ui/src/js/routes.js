// Blank page for login background
import HomePage from '../pages/home.f7.html';

// Setup pages
import IPFireSetup from '../pages/setup/ipfire.f7.html';
import AdminSetup from '../pages/setup/admin.f7.html';

// General pages
import WelcomePage from '../pages/welcome.f7.html';

// Users pages
import UserList from '../pages/users/list.f7.html';
import ChangeUser from '../pages/users/change.f7.html';
import CreateUser from '../pages/users/create.f7.html';
import ImportUsers from '../pages/users/import.f7.html';
import ImportLUSDUsers from '../pages/users/lusd.f7.html';
import TransferLUSDUsers from '../pages/users/transfer.f7.html';
import IntegrityCheck from '../pages/users/integritycheck.f7.html';

// Groups pages
import GroupList from '../pages/groups/list.f7.html';
import ChangeGroup from '../pages/groups/change.f7.html';
import CreateGroup from '../pages/groups/create.f7.html';

// Share pages
import ShareList from '../pages/shares/list.f7.html';
import ChangeShare from '../pages/shares/change.f7.html';
import CreateShare from '../pages/shares/create.f7.html';

// Device pages
import DevicesList from '../pages/devices/list.f7.html';
import ChangeDevice from '../pages/devices/change.f7.html';
import InstallClient from '../pages/devices/install.f7.html';

// Profiles pages
import ProfilesList from '../pages/profiles/list.f7.html';
import ChangeProfile from '../pages/profiles/change.f7.html';
import CreateProfile from '../pages/profiles/create.f7.html';

// Server pages
import ServerOverview from '../pages/server/overview.f7.html';
import ServerPlugins from '../pages/server/plugins.f7.html';
import ServerSettings from '../pages/server/settings.f7.html';
import IPFireSettings from '../pages/server/ipfire.f7.html';
import InstallPlugin from '../pages/server/installation.f7.html';
import UpdatePlugin from '../pages/server/update.f7.html';

import NotFoundPage from '../pages/404.f7.html';

var routes = [
  {
    path: '/',
    component: HomePage,
  },
  {
    path: '/setup/ipfire',
    component: IPFireSetup,
  },
  {
    path: '/setup/admin',
    component: AdminSetup,
  },
  {
    path: '/welcome',
    component: WelcomePage,
  },
  {
    path: '/users',
    component: UserList,
  },
  {
    path: '/users/create',
    component: CreateUser,
  },
  {
    path: '/users/import',
    component: ImportUsers,
  },
  {
    path: '/users/lusdimport',
    component: ImportLUSDUsers,
  },
  {
    path: '/users/transfer',
    component: TransferLUSDUsers,
  },
  {
    path: '/users/integritycheck',
    component: IntegrityCheck,
  },
  {
    path: '/users/:id',
    component: ChangeUser,
  },
  {
    path: '/groups',
    component: GroupList,
  },
  {
    path: '/groups/create',
    component: CreateGroup,
  },
  {
    path: '/groups/:id',
    component: ChangeGroup,
  },
  {
    path: '/shares',
    component: ShareList,
  },
  {
    path: '/shares/create',
    component: CreateShare,
  },
  {
    path: '/shares/:id',
    component: ChangeShare,
  },
  {
    path: '/devices',
    component: DevicesList,
  },
  {
    path: '/devices/install',
    component: InstallClient,
  },
  {
    path: '/devices/:id',
    component: ChangeDevice,
  },
  {
    path: '/profiles',
    component: ProfilesList,
  },
  {
    path: '/profiles/create',
    component: CreateProfile,
  },
  {
    path: '/profiles/:id',
    component: ChangeProfile,
  },
  {
    path: '/server',
    component: ServerOverview,
  },
  {
    path: '/server/plugins',
    component: ServerPlugins,
  },
  {
    path: '/server/settings',
    component: ServerSettings,
  },
  {
    path: '/server/ipfire',
    component: IPFireSettings,
  },
  {
    path: '/server/plugins/install/:name',
    component: InstallPlugin,
  },
  {
    path: '/server/plugins/update/:name/:version',
    component: UpdatePlugin,
  },
  {
    path: '(.*)',
    component: NotFoundPage,
  },
];

export default routes;
